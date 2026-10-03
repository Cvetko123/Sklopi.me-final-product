#Aleksandar Cvetkovic 2023/0150
"""
Modul za koordinaciju procesa skejpovanja

**Opis:**

Sadrži glavni servis koji koordinira ceo proces skejpovanja od preuzianja podataka
do fuzzy matchinga i čuvanja u bazi podataka.
"""


class ScraperService:
    """
    Servis za koordinaciju skejpovanja.
    
    Integrira skejper, fuzzy matcher i database servis u jedinstveni proces.
    """
    
    def __init__(self, scraper, fuzzy_matcher, db_service):
        """
        Inicijalizuje ScraperService sa potrebnim komponentama.
        
        :param scraper: Instanca skejpera koji prikuplja podatke
        :type scraper: BaseScraper
        :param fuzzy_matcher: Instanca fuzzy matchera koji upoređuje proizvode
        :type fuzzy_matcher: FuzzyMatcher
        :param db_service: Servis za čuvanje podataka u bazi
        :type db_service: ComponentService
        """
        self.scraper = scraper
        self.fuzzy_matcher = fuzzy_matcher
        self.db_service = db_service

    def load_data(self):
        """
        Izvršava ceo proces skrejpovanja i čuvanja podataka.
        
        Koraci:
        1. Skrejpuje proizvode sa veb-sajta
        2. Primenjuje fuzzy matching da pronađe odgovarajuće komponente u bazi
        3. Čuva cene filtrirane komponente u bazi podataka
        
        :return: Tuple (uspeh, broj_sačuvanih_proizvoda)
        :rtype: tuple(bool, int)
        """
        products = self.scraper.scrape()
        filterd_products = self.fuzzy_matcher.match(products)
        if not filterd_products:
            return False,0
        for prod in filterd_products:
            self.db_service.save(prod)
        return True, len(filterd_products)







