# Marko Ciric 2023/0133 - SSU 4.2: LLM provider apstrakcija (DIP)

"""
LLMProvider je apstraktna granica između view sloja i konkretnog dobavljača
jezičkog modela. Views i ConfiguratorService zavise samo od ovog interfejsa
(parse_user_request), tako da zamena OpenAI -> Anthropic -> Ollama -> HuggingFace
ne zahteva izmene bilo gde drugde u kodu (Dependency Inversion Principle).

Ugovor (Section 4 master prompta) - parse_user_request MORA da vrati rečnik
jednog od dva oblika:

Varijanta 1 (pojedinačna komponenta):
{
    "action": "recommend_component",
    "component_type": "gpu",
    "filters": {"manufacturer": "Nvidia", "price_max": 50000, ...}
}

Varijanta 2 (cela konfiguracija):
{
    "action": "suggest_full_build",
    "budget": 120000,
    "use_case": "gaming"
}

Ili, ako zahtev nije razumljiv / nema veze sa namenom konfiguratora:
{
    "action": "invalid_request",
    "reason": "<kratko objašnjenje>"
}
"""

import json
from abc import ABC, abstractmethod

VALID_COMPONENT_TYPES = {'cpu', 'cpucooler', 'motherboard', 'ram', 'storage', 'gpu', 'case', 'powersupply'}
VALID_USE_CASES = {'gaming', 'development', 'work_office'}
VALID_ACTIONS = {'recommend_component', 'suggest_full_build', 'invalid_request'}


class LLMParsingError(Exception):
    """Izuzetak koji ukazuje na grešku prilikom parsiranja ili validacije strukture odgovora LLM-a."""
    pass


SYSTEM_PROMPT = """Ti si asistent za konfigurator PC komponenti sajta Sklopi.me.
Tvoj jedini zadatak je da korisnički tekst na srpskom (ili engleskom) pretvoriš
u STROGO validan JSON, bez ikakvog dodatnog teksta, markdown ograda ili objašnjenja.

Podržane vrste komponenti (component_type): cpu, cpucooler, motherboard, ram, storage, gpu, case, powersupply
Podržane namene (use_case): gaming, development, work_office

Ako korisnik traži jednu vrstu komponente, vrati:
{"action": "recommend_component", "component_type": "<tip>", "filters": {...}}
Dozvoljeni ključevi u filters: manufacturer, price_min, price_max, i specifični
atributi komponente (npr. socket, memcapacity, wattage...).

Ako korisnik traži celu konfiguraciju / build, vrati:
{"action": "suggest_full_build", "budget": <broj ili null>, "use_case": "<tip ili null>"}

Ako zahtev nema nikakve veze sa kupovinom/pretragom PC komponenti, vrati:
{"action": "invalid_request", "reason": "<kratak razlog>"}

Vrati ISKLJUČIVO JSON objekat, ništa drugo."""


class LLMProvider(ABC):
    """
        Apstraktna klasa (interfejs) za LLM provajdere

        **Opis:**

        Definiše granicu između aplikativnog sloja i konkretnih implementacija
        veštačke inteligencije u skladu sa Dependency Inversion principom.
    """
    @abstractmethod
    def parse_user_request(self, user_text: str) -> dict:
        """
            Apstraktna metoda za prevođenje teksta u struktuirani rečnik

            :param user_text: Tekstualni unos korisnika sa prirodnog jezika.
            :return: Validiran rečnik sa akcijom i izvučenim filtrima.
        """
        raise NotImplementedError

    def _validate_schema(self, payload: dict) -> dict:
        """
            Validacija šeme i vrednosti izlaznog JSON-a

            **Opis:**

            Proverava da li generisani odgovor sadrži dozvoljene akcije, validne tipove
            komponenti i ispravne tipove podataka za budžet i namenu.

            :param payload: Sirovi rečnik dobijen dekodiranjem modelovog odgovora.
            :return: Validiran i očišćen rečnik spreman za servis konfiguratora.
        """
        if not isinstance(payload, dict) or 'action' not in payload:
            raise LLMParsingError('Odgovor modela nije u očekivanom formatu.')

        action = payload.get('action')
        if action not in VALID_ACTIONS:
            raise LLMParsingError(f'Nepoznata akcija: {action!r}')

        if action == 'recommend_component':
            component_type = payload.get('component_type')
            if component_type not in VALID_COMPONENT_TYPES:
                raise LLMParsingError(f'Nepoznat tip komponente: {component_type!r}')
            payload.setdefault('filters', {})
            if not isinstance(payload['filters'], dict):
                raise LLMParsingError("Polje 'filters' mora biti objekat.")

        elif action == 'suggest_full_build':
            budget = payload.get('budget')
            if budget is not None:
                try:
                    payload['budget'] = int(budget)
                except (TypeError, ValueError):
                    raise LLMParsingError("Polje 'budget' mora biti broj.")
            use_case = payload.get('use_case')
            if use_case is not None and use_case not in VALID_USE_CASES:
                payload['use_case'] = None

        return payload


class OpenAILLMProvider(LLMProvider):
    """
        Konkretna implementacija LLM provajdera preko OpenAI API-ja

        **Opis:**

        Komunicira sa zvaničnim OpenAI GPT modelima (podrazumevano gpt-4o-mini)
        koristeći JSON mod kako bi garantovao povratnu strukturu. Sada sadrži
        i retry logiku sa eksponencijalnim kašnjenjem za free tier rate limite.
    """

    def __init__(self, client=None, model: str = 'gpt-4o-mini', max_retries: int = 4, initial_delay: float = 1.0):
        """
            Inicijalizacija provajdera sa klijentom i imenom modela

            :param client: Instanca OpenAI klijenta.
            :param model: String naziv modela koji se poziva.
            :param max_retries: Maksimalan broj ponovnih pokušaja u slučaju Rate Limita.
            :param initial_delay: Početno vreme čekanja u sekundama.
        """
        self._client = client
        self._model = model
        self._max_retries = max_retries
        self._initial_delay = initial_delay

    def parse_user_request(self, user_text: str) -> dict:
        """
            Slanje teksta OpenAI API-ju i strukturiranje rezultata

            **Opis:**

            Kreira poziv ka Chat Completions endpoint-u sa predefinisanim sistemskim
            uputstvima i tekstom korisnika, a dobijeni tekst konvertuje u rečnik uz validaciju.

            :param user_text: Tekstualni upit korisnika.
            :return: Validiran rečnik sa parametrima zahteva.
        """
        if self._client is None:
            raise LLMParsingError(
                'OpenAI klijent nije konfigurisan. Prosledite ga kroz konstruktor '
                'ili koristite MockLLMProvider za razvoj/testiranje.'
            )

        delay = self._initial_delay
        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    response_format={'type': 'json_object'},
                    messages=[
                        {'role': 'system', 'content': SYSTEM_PROMPT},
                        {'role': 'user', 'content': user_text},
                    ],
                )
                raw_content = response.choices[0].message.content
                break

            except Exception as exc:
                import openai
                import random
                import time
                is_rate_limit = False
                if isinstance(exc, openai.RateLimitError):
                    is_rate_limit = True
                elif "429" in str(exc) or "rate limit" in str(exc).lower():
                    is_rate_limit = True

                if is_rate_limit and attempt < self._max_retries:
                    actual_delay = delay * (2 ** attempt) + random.uniform(0.5, 1.5)

                    print(f"[OpenAI Provider] Rate limit hit. Pokušaj {attempt + 1}/{self._max_retries}. "
                          f"Čekam {actual_delay:.2f}s pre ponovnog pokušaja...")

                    time.sleep(actual_delay)
                    continue

                # Ako nije rate limit, ili smo ispucali sve pokušaje, baci konačnu grešku
                raise LLMParsingError(f'Greška u komunikaciji sa LLM servisom: {exc}')

        try:
            payload = json.loads(raw_content)
        except (json.JSONDecodeError, TypeError):
            raise LLMParsingError('Model nije vratio validan JSON.')

        return self._validate_schema(payload)


class MockLLMProvider(LLMProvider):
    """
        Mock implementacija LLM provajdera za lokalno testiranje i razvoj

        **Opis:**

        Ne šalje mrežne zahteve spoljnim servisima, već na osnovu predefinisanih ključnih reči
        i regularnih izraza simulira ponašanje veštačke inteligencije na srpskom jeziku.
    """
    _KEYWORDS = {
        'cpu': ('procesor', 'cpu'),
        'cpucooler': ('hladnjak', 'cooler'),
        'motherboard': ('matičn', 'maticn', 'ploč', 'motherboard'),
        'ram': ('ram', 'memorij'),
        'storage': ('disk', 'ssd', 'hdd', 'storage'),
        'gpu': ('grafičk', 'graficka', 'gpu', 'video kartic'),
        'case': ('kućišt', 'kuciste', 'case'),
        'powersupply': ('napajanj', 'powersupply', 'power supply'),
    }
    _USE_CASE_KEYWORDS = {
        'gaming': ('gaming', 'igranje', 'igric'),
        'development': ('development', 'razvoj', 'programiranj', 'dev'),
        'work_office': ('kancelarij', 'office', 'posao'),
    }

    def parse_user_request(self, user_text: str) -> dict:
        """
            Simulacija parsiranja upita analizom ključnih reči

            **Opis:**

            Pretražuje tekst na prisustvo reči kao što su 'grafička', 'procesor', 'gaming', 'budžet'
            i sklapa JSON odgovor koji oponaša pravi jezički model.

            :param user_text: Tekstualni upit korisnika.
            :return: Validiran rečnik generisan heurističkom analizom reči.
        """
        text = user_text.lower().strip()
        if not text:
            payload = {'action': 'invalid_request', 'reason': 'Prazan zahtev.'}
            return self._validate_schema(payload)

        if 'konfiguraciju' in text or 'build' in text or 'ceo računar' in text or 'ceo racunar' in text:
            payload = {
                'action': 'suggest_full_build',
                'budget': self._extract_price(text, keyword=None),
                'use_case': self._extract_use_case(text),
            }
            return self._validate_schema(payload)

        component_type = self._extract_component_type(text)
        if component_type is None:
            payload = {
                'action': 'invalid_request',
                'reason': 'Zahtev nije prepoznat kao pretraga PC komponenti.',
            }
            return self._validate_schema(payload)

        payload = {
            'action': 'recommend_component',
            'component_type': component_type,
            'filters': {
                'price_max': self._extract_price(text, keyword='ispod'),
                'manufacturer': self._extract_manufacturer(text),
            },
        }
        payload['filters'] = {k: v for k, v in payload['filters'].items() if v is not None}
        return self._validate_schema(payload)

    def _extract_component_type(self, text):
        for component_type, keywords in self._KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return component_type
        return None

    def _extract_use_case(self, text):
        for use_case, keywords in self._USE_CASE_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return use_case
        return None

    def _extract_price(self, text, keyword):
        import re
        match = re.search(r'(\d[\d.]{2,})\s*(rsd|din)?', text)
        if not match:
            return None
        digits = match.group(1).replace('.', '')
        try:
            return int(digits)
        except ValueError:
            return None

    def _extract_manufacturer(self, text):
        for brand in ('nvidia', 'amd', 'intel', 'asus', 'msi', 'gigabyte', 'corsair'):
            if brand in text:
                return brand.capitalize()
        return None