#Aleksandar Cvetkovic 2023/0150
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """
    Apstraktna bazna klasa za sve web skejpere.
    
    Definiše osnovni interfejs koji svi skrejperi moraju da implementiraju.
    """

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def scrape(self):
        """
        Apstraktna metoda za skejpovanje. Mora biti implementirana od strane podklasa.
        
        :return: Lista skejpovanih proizvoda
        """