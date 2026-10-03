# Marko Ciric 2023/0133

from django.db.models import Count, Min

from .compatibility import CompatibilityValidator
from .heuristics import BudgetAllocator
from .llm import LLMParsingError

MAX_RESULTS_PER_CATEGORY = 5


class ConfiguratorError(Exception):
    """Bazna klasa za izuzetke servisa konfiguratora."""
    pass


class InvalidRequestError(ConfiguratorError):
    """Izuzetak koji se ispaljuje kada je korisnički zahtev nerazumljiv ili nevalidan."""
    pass


class NoResultsError(ConfiguratorError):
    """Izuzetak koji se ispaljuje kada nijedna komponenta ne zadovoljava kriterijume pretrage."""
    pass


class ConfiguratorService:
    """
        Glavni servis za upravljanje logikom pametnog konfiguratora

        **Opis:**

        Kordinira procesom parsiranja korisničkog unosa putem LLM-a, raspodelom budžeta
        preko heurističkog algoritma i filtriranjem kompatibilnog hardvera.
    """
    def __init__(self, llm_provider, compatibility_validator: CompatibilityValidator = None,
                 budget_allocator: BudgetAllocator = None):
        """
            Inicijalizacija servisa sa neophodnim provajderima i komponentama

            :param llm_provider: Instanca klase koja implementira interfejs LLMProvider.
            :param compatibility_validator: Validator kompatibilnosti (opciono, podrazumeva novu instancu).
            :param budget_allocator: Alokator budžeta (opciono, podrazumeva novu instancu).
        """
        self._llm = llm_provider
        self._compatibility = compatibility_validator or CompatibilityValidator()
        self._budget_allocator = budget_allocator or BudgetAllocator()

    def handle_message(self, user_text: str, current_build: dict) -> dict:
        """
            Glavna ulazna tačka za obradu korisničke poruke

            **Opis:**

            Uzima tekstualnu poruku, šalje je na parsiranje jezičkom modelu, a zatim
            na osnovu prepoznate akcije usmerava izvršavanje na preporuku pojedinačne
            komponente ili sastavljanje cele konfiguracije.

            :param user_text: Tekstualna poruka korisnika iz četa.
            :param current_build: Rečnik sa trenutno izabranim komponentama iz sesije.
            :return: Rečnik sa tekstualnim odgovorom i strukturiranim preporukama za klijenta.
        """
        try:
            parsed = self._llm.parse_user_request(user_text)
        except LLMParsingError as exc:
            raise InvalidRequestError(str(exc))

        action = parsed['action']

        if action == 'invalid_request':
            raise InvalidRequestError(parsed.get('reason', 'Zahtev nije prepoznat.'))

        if action == 'recommend_component':
            return self._handle_recommend_component(parsed, current_build)

        if action == 'suggest_full_build':
            return self._handle_suggest_full_build(parsed, current_build)

        raise InvalidRequestError(f'Nepodržana akcija: {action}')

    def _handle_recommend_component(self, parsed: dict, current_build: dict) -> dict:
        """
            Interna obrada zahteva za preporuku specifičnog tipa komponente

            **Opis:**

            Vrši upit nad bazom podataka za traženi tip komponente primenjujući
            izvučene filtere i proveravajući kompatibilnost sa trenutnim build-om.

            :param parsed: Rečnik sa parsiranim parametrima i filterima od strane LLM-a.
            :param current_build: Rečnik sa trenutnim stanjem konfiguracije.
            :return: Rečnik sa porukom o uspehu i listom preporučenih komponenti.
        """
        component_type = parsed['component_type']
        filters = parsed.get('filters', {})

        results = self._query_components(component_type, filters, current_build)
        if not results:
            raise NoResultsError(
                'Nisu pronađene komponente koje zadovoljavaju zadate kriterijume i '
                'kompatibilne su sa trenutnom konfiguracijom.'
            )

        return {
            'message': f'Pronašao sam {len(results)} predloga.',
            'recommendations': results,
        }

    def _handle_suggest_full_build(self, parsed: dict, current_build: dict) -> dict:
        """
            Interna obrada zahteva za generisanje kompletne konfiguracije u okviru budžeta

            **Opis:**

            Pokreće heurističku raspodelu ukupnog budžeta po kategorijama na osnovu namene
            računara, a zatim iterativno pronalazi i slaže prve najpopularnije kompatibilne
            komponente u svakoj kategoriji.

            :param parsed: Rečnik sa unetim budžetom i namenom računara.
            :param current_build: Rečnik sa trenutnim stanjem konfiguracije.
            :return: Rečnik sa preporučenim komponentama grupisanim po kategorijama hardvera.
        """
        budget = parsed.get('budget')
        use_case = parsed.get('use_case')

        from .views import COMPONENT_DICT
        category_budgets = (
            self._budget_allocator.allocate(budget, use_case)
            if budget else {category: None for category in COMPONENT_DICT}
        )

        build_so_far = dict(current_build)
        recommendations_by_category = {}
        missing_categories = []

        for component_type, max_price in category_budgets.items():
            filters = {'price_max': max_price} if max_price else {}
            candidates = self._query_components(
                component_type, filters, build_so_far, limit=1
            )
            if candidates:
                recommendations_by_category[component_type] = candidates
                model = COMPONENT_DICT[component_type]['model']
                build_so_far[component_type] = model.objects.filter(
                    pk=candidates[0]['component'].id
                ).first()
            else:
                missing_categories.append(component_type)

        if not recommendations_by_category:
            raise NoResultsError(
                'Nije bilo moguće sastaviti nijednu kompatibilnu komponentu u okviru zadatog budžeta.'
            )

        message = 'Evo predloga konfiguracije na osnovu zadatog budžeta.'
        if missing_categories:
            message += (
                ' Napomena: za sledeće kategorije nisam našao odgovarajuću komponentu '
                f'u okviru budžeta: {", ".join(missing_categories)}.'
            )

        return {
            'message': message,
            'recommendations_by_category': recommendations_by_category,
        }

    def _query_components(self, component_type: str, filters: dict, current_build: dict, limit: int = MAX_RESULTS_PER_CATEGORY):
        """
            Dohvatanje, filtriranje i sortiranje komponenti iz baze podataka

            **Opis:**

            Kreira bazni QuerySet za određeni model komponente, računa minimalnu cenu iz
            povezanih prodavnica, računa indeks popularnosti (broj ugradnji u gotove računare),
            primenjuje dinamičke i statičke filtere, sortira rezultate po popularnosti i ceni,
            te na kraju propušta rezultate kroz validator kompatibilnosti.

            :param component_type: String oznaka tipa komponente (npr. 'gpu', 'cpu').
            :param filters: Rečnik sa izvučenim filterima (npr. proizvođač, opseg cena).
            :param current_build: Trenutno sastavljena konfiguracija radi provere kompatibilnosti.
            :param limit: Maksimalan broj rezultata koji se vraća po kategoriji.
            :return: Lista rečnika sa serijalizovanim podacima o kompatibilnim komponentama.
        """
        from .views import COMPONENT_DICT

        if component_type not in COMPONENT_DICT:
            raise InvalidRequestError(f'Nepoznat tip komponente: {component_type}')

        model = COMPONENT_DICT[component_type]['model']
        queryset = model.objects.annotate(
            min_price=Min('componentprice__price'),
            popularity=Count('buildcomponent', distinct=True),
        ).exclude(min_price__isnull=True)

        manufacturer = filters.get('manufacturer')
        if manufacturer:
            queryset = queryset.filter(manufacturer__iexact=manufacturer)

        price_min = filters.get('price_min')
        if price_min:
            queryset = queryset.filter(min_price__gte=price_min)

        price_max = filters.get('price_max')
        if price_max:
            queryset = queryset.filter(min_price__lte=price_max)

        for key, value in filters.items():
            if key in ('manufacturer', 'price_min', 'price_max'):
                continue
            if hasattr(model, key):
                queryset = queryset.filter(**{f'{key}__iexact': value})

        queryset = queryset.order_by('-popularity', 'min_price')[: limit * 3]

        compatible = self._compatibility.filter_compatible(component_type, queryset, current_build)
        compatible = compatible[:limit]

        return [
            {
                'component': component,
                'component_type': component_type,
                'name': component.name,
                'manufacturer': component.manufacturer,
                'price': component.min_price,
                'price_display': f'{component.min_price} RSD',
            }
            for component in compatible
        ]