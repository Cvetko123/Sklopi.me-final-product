#Aleksandar Cvetkovic 2023/0150
"""
Django upravljačka komanda za skejpovanje cena komponenti

**Opis:**

Definiše Django upravljačku komandu koja omogućava skejpovanje cena računarskih komponenti
sa različitih prodavnica. Komanda je dostupna kroz: `python manage.py scrape_store --url <url> --store <store> --type <type>`

**Argumenti komande:**

- `--url`: URL stranice prodavnice koja se skejpuje (obavezno)
- `--store`: Naziv prodavnice (obavezno, podržani: gigatron, computerland)
- `--type`: Tip komponente (obavezno, podržani: cpu, gpu, ram, motherboard, storage, cooler, psu, case)
"""
from django.core.management.base import BaseCommand


from scraper.services.componentprice_service import ComponentService
from scraper.services.scraper_service import ScraperService
from scraper.scrapers.computerland_scraper import ComputerlandScraper
from scraper.scrapers.gigatron_scraper import GigatronScraper
from scraper.util.fuzzy_matcher import FuzzyMatcher

SCRAPERS={
    'gigatron':GigatronScraper,
    'computerland':ComputerlandScraper,
}
from app.models import (
    Cpu,
    Gpu,
    Ram,
    Motherboard,
    Storage,
    Cpucooler,
    Powersupply,
    Case,
)



MODELS = {
    "cpu": Cpu,
    "gpu": Gpu,
    "ram": Ram,
    "motherboard": Motherboard,
    "storage": Storage,
    "cooler": Cpucooler,
    "psu": Powersupply,
    "case": Case,
}

class Command(BaseCommand):
    """
    Django upravljačka komanda za skrejpovanje cena komponenti.
    
    Omogućava korisniku da skrejpuje cene komponenti sa različitih prodavnica
    kroz komandnu liniju sa specificiranim parametrima.
    """
    
    def add_arguments(self, parser):
        """
        Definiše argumenti komande.
        
        :param parser: Argument parser
        """
        parser.add_argument('--url', type=str, help='Url of the store page for desired component type')
        parser.add_argument('--store', type=str, help='Store corresponding to the url')
        parser.add_argument('--type', type=str, help='Type of the component you want to scrape')

    def handle(self, *args, **options):
        """
        Izvršava skrejpovanje sa zadatim parametrima.
        
        Validira sve obavezne argumente, pronalazi odgovarajući skejper i fuzzy matcher,
        i izvršava kompletno skejpovanje sa čuvanjem u bazu podataka.
        
        :param args: Poziski argumenti
        :param options: Argumenti komande (url, store, type)
        """

        url = options['url']
        store = options['store']
        component_type = options['type']
        if url is None:
            self.stderr.write(self.style.ERROR("Url is required."))
            return
        if store is None:
            self.stderr.write(self.style.ERROR("Store is required."))
            return
        if component_type is None:
            self.stderr.write(self.style.ERROR("Type is required."))



        if store not in SCRAPERS:
            self.stderr.write(self.style.ERROR(f"Store '{store}' is not supported."))
            return
        if component_type not in MODELS:
            self.stderr.write(self.style.ERROR(f"Type'{component_type}' is not supported or does not exist."))
            return

        scraper_class = SCRAPERS[store]
        scraper = scraper_class(url=url)
        fuzzy_matcher = FuzzyMatcher(component_type)
        db_service= ComponentService()
        service = ScraperService(scraper,fuzzy_matcher,db_service)
        ok,num_added = service.load_data()
        if ok:
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {num_added} prices for {component_type} from {store}."))
        else:
            self.stderr.write(self.style.ERROR(f"Failed to load data for {component_type} from {store}."))
