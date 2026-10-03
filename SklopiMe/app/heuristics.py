# Marko Ciric 2023/0133

"""
Statička procentualna raspodela budžeta po kategoriji komponenti, u zavisnosti
od namene računara (2.1 iz SSU dokumenta).
"""

DEFAULT_USE_CASE = 'gaming'

BUDGET_HEURISTICS = {
    'gaming': {
        'gpu': 0.38, 'cpu': 0.20, 'motherboard': 0.10, 'ram': 0.10,
        'storage': 0.08, 'powersupply': 0.08, 'case': 0.04, 'cpucooler': 0.02,
    },
    'development': {
        'gpu': 0.15, 'cpu': 0.33, 'motherboard': 0.15, 'ram': 0.20,
        'storage': 0.10, 'powersupply': 0.07, 'case': 0.03, 'cpucooler': 0.02,
    },
    'work_office': {
        'gpu': 0.05, 'cpu': 0.30, 'motherboard': 0.15, 'ram': 0.15,
        'storage': 0.20, 'powersupply': 0.10, 'case': 0.10, 'cpucooler': 0.02,
    },
}


class BudgetAllocator:
    """
        Heuristički alokator budžeta za PC komponente

        **Opis:**

        Računa raspodelu novčanih sredstava po pojedinačnim hardverskim kategorijama
        u zavisnosti od primarne namene računara (gaming, programiranje ili kancelarijski rad).
    """

    def __init__(self, heuristics: dict = None):
        """
            Inicijalizacija alokatora sa predefinisanim težinama

            :param heuristics: Opcioni rečnik sa prilagođenim heurističkim težinama.
        """
        self._heuristics = heuristics or BUDGET_HEURISTICS

    def allocate(self, budget: int, use_case: str = None) -> dict:
        """
            Izračunavanje maksimalnog budžeta za svaku komponentu

            **Opis:**

            Uzima ukupnu sumu i množi je sa procentualnim udelom specifične komponente
            definisanom u matrici težina za prosleđeni use_case.

            :param budget: Ukupan celobrojni budžet za ceo računar.
            :param use_case: String oznaka namene konfiguracije ('gaming', 'development', 'work_office').
            :return: Rečnik gde su ključevi tipovi komponenti, a vrednosti izračunata maksimalna cena.
        """
        weights = self._heuristics.get(use_case) or self._heuristics[DEFAULT_USE_CASE]
        total_weight = sum(weights.values())

        return {
            component_type: int(budget * (weight / total_weight))
            for component_type, weight in weights.items()
        }