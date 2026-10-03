# Marko Ciric 2023/0133

"""
Pravila:
1. CPU <-> Matična ploča: socket mora biti identičan.
2. Matična ploča <-> RAM: tip memorije mora da se poklapa i broj modula ne
   sme da pređe broj raspoloživih slotova.
3. Matična ploča <-> Kućište: kućište mora da podržava format matične ploče.
4. Napajanje: zbir potrošnje (powerconsumption) svih odabranih komponenti
   (uključujući kandidata) ne sme da pređe deklarisanu snagu napajanja.
"""

from dataclasses import dataclass


@dataclass
class CompatibilityResult:
    """
        Struktura podataka za rezultat provere kompatibilnosti

        **Opis:**

        Sadrži logičku vrednost koja označava da li su komponente kompatibilne i
        tekstualno obrazloženje ukoliko je detektovan konflikt.
    """
    compatible: bool
    reason: str = ''


class CompatibilityValidator:
    """
        Validator kompatibilnosti PC komponenti

        **Opis:**

        Sadrži logiku za proveru hardverske usklađenosti između procesora, matičnih ploča,
        RAM memorije, kućišta i energetskog budžeta napajanja.
    """
    def is_compatible(self, component_type: str, candidate, current_build: dict) -> CompatibilityResult:
        """
            Provera kompatibilnosti jedne komponente sa trenutnom konfiguracijom

            **Opis:**

            Prolazi kroz niz sekvencijalnih provera (soket, memorija, format, napajanje)
            kako bi utvrdio da li kandidat zadovoljava sve uslove kompatibilnosti sa ostatkom računara.

            :param component_type: String oznaka tipa komponente kandidata (npr. 'cpu', 'ram').
            :param candidate: Objekat modela komponente koja se proverava.
            :param current_build: Rečnik sa trenutno izabranim komponentama u konfiguraciji.
            :return: CompatibilityResult objekat sa ishodom i potencijalnim razlogom nekompatibilnosti.
        """
        checks = (
            self._check_cpu_motherboard,
            self._check_motherboard_ram,
            self._check_motherboard_case,
            self._check_power_budget,
        )

        for check in checks:
            result = check(component_type, candidate, current_build)
            if not result.compatible:
                return result

        return CompatibilityResult(compatible=True)

    def filter_compatible(self, component_type: str, candidates, current_build: dict):
        """
            Filtriranje liste kandidata na osnovu kompatibilnosti

            **Opis:**

            Prima listu potencijalnih komponenti i vraća samo one koje su potpuno
            kompatibilne sa trenutnim stanjem računara.

            :param component_type: String oznaka tipa komponente.
            :param candidates: Iterabilna kolekcija objekata komponenti (QuerySet ili lista).
            :param current_build: Rečnik sa trenutno izabranim komponentama.
            :return: Lista kompatibilnih objekata komponenti.
        """
        return [
            candidate for candidate in candidates
            if self.is_compatible(component_type, candidate, current_build).compatible
        ]

    def _check_cpu_motherboard(self, component_type, candidate, current_build):
        """
            Interna provera kompatibilnosti ležišta (soketa) procesora i matične ploče

            **Opis:**

            Proverava da li se vrednost polja 'socket' na procesoru poklapa sa istim poljem na matičnoj ploči.

            :param component_type: String oznaka tipa komponente kandidata.
            :param candidate: Objekat komponente koja se proverava.
            :param current_build: Rečnik sa trenutnim build-om.
            :return: CompatibilityResult sa ishodom provere.
        """
        cpu = candidate if component_type == 'cpu' else current_build.get('cpu')
        motherboard = candidate if component_type == 'motherboard' else current_build.get('motherboard')

        if cpu is None or motherboard is None:
            return CompatibilityResult(compatible=True)

        if cpu.socket != motherboard.socket:
            return CompatibilityResult(
                compatible=False,
                reason=f'Soket procesora ({cpu.socket}) ne odgovara soketu matične ploče ({motherboard.socket}).',
            )
        return CompatibilityResult(compatible=True)

    def _check_motherboard_ram(self, component_type, candidate, current_build):
        """
            Interna provera kompatibilnosti RAM memorije i matične ploče

            **Opis:**

            Proverava da li se generacija memorije poklapa sa podržanom na ploči (npr. DDR4, DDR5)
            i da li broj fizičkih modula RAM-a prelazi broj slobodnih slotova na ploči.

            :param component_type: String oznaka tipa komponente kandidata.
            :param candidate: Objekat komponente koja se proverava.
            :param current_build: Rečnik sa trenutnim build-om.
            :return: CompatibilityResult sa ishodom provere.
        """
        motherboard = candidate if component_type == 'motherboard' else current_build.get('motherboard')
        ram = candidate if component_type == 'ram' else current_build.get('ram')

        if motherboard is None or ram is None:
            return CompatibilityResult(compatible=True)

        if motherboard.ramtype != ram.type:
            return CompatibilityResult(
                compatible=False,
                reason=f'Tip memorije ({ram.type}) ne odgovara tipu koji podržava ploča ({motherboard.ramtype}).',
            )

        if ram.modulenum > motherboard.ramslots:
            return CompatibilityResult(
                compatible=False,
                reason=(
                    f'RAM zahteva {ram.modulenum} modula, a matična ploča ima '
                    f'samo {motherboard.ramslots} slotova.'
                ),
            )
        return CompatibilityResult(compatible=True)

    def _check_motherboard_case(self, component_type, candidate, current_build):
        """
            Interna provera kompatibilnosti formata matične ploče i kućišta

            **Opis:**

            Proverava da li kućište podržava faktor oblika matične ploče (npr. ATX, Micro-ATX)
            tako što pretražuje zapetom razdvojenu listu podržanih formata u kućištu.

            :param component_type: String oznaka tipa komponente kandidata.
            :param candidate: Objekat komponente koja se proverava.
            :param current_build: Rečnik sa trenutnim build-om.
            :return: CompatibilityResult sa ishodom provere.
        """
        motherboard = candidate if component_type == 'motherboard' else current_build.get('motherboard')
        case = candidate if component_type == 'case' else current_build.get('case')

        if motherboard is None or case is None:
            return CompatibilityResult(compatible=True)

        supported_formats = [fmt.strip().upper() for fmt in case.supportedmotherboards.split(',')]
        if motherboard.formfactor.strip().upper() not in supported_formats:
            return CompatibilityResult(
                compatible=False,
                reason=(
                    f'Kućište ne podržava format matične ploče '
                    f'({motherboard.formfactor}); podržani formati: {case.supportedmotherboards}.'
                ),
            )
        return CompatibilityResult(compatible=True)

    def _check_power_budget(self, component_type, candidate, current_build):
        """
            Interna provera energetskog budžeta konfiguracije

            **Opis:**

            Sabira deklarisanu potrošnju struje svih selektovanih komponenti i proverava
            da li ukupna vrednost (u vatima) prelazi maksimalnu snagu izabranog napajanja.

            :param component_type: String oznaka tipa komponente kandidata.
            :param candidate: Objekat komponente koja se proverava.
            :param current_build: Rečnik sa trenutnim build-om.
            :return: CompatibilityResult sa ishodom provere.
        """
        psu = candidate if component_type == 'powersupply' else current_build.get('powersupply')
        if psu is None:
            return CompatibilityResult(compatible=True)

        total_consumption = 0
        for existing_type, existing_component in current_build.items():
            if existing_type in ('powersupply',) or existing_component is None:
                continue
            if existing_type == component_type:
                continue
            total_consumption += existing_component.powerconsumption or 0

        if component_type != 'powersupply':
            total_consumption += candidate.powerconsumption or 0

        if total_consumption > psu.wattage:
            return CompatibilityResult(
                compatible=False,
                reason=(
                    f'Ukupna potrošnja komponenti ({total_consumption}W) prelazi '
                    f'snagu napajanja ({psu.wattage}W).'
                ),
            )
        return CompatibilityResult(compatible=True)