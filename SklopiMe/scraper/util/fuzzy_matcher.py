#Aleksandar Cvetkovic 2023/0150
from rapidfuzz import fuzz
from scraper.util.schemas import FuzzyFilteredProduct

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

from scraper.util.normalizers import *

NORMALIZERS = {
    "cpu": normalize_cpu_name,
    "gpu": normalize_gpu_name,
    "storage": normalize_storage_name,
    "motherboard": normalize_motherboard_name,
    "ram": normalize_ram_name,
    "cooler": normalize_cooler_name,
    "psu": normalize_psu_name,
    "case": normalize_case_name,
}


class FuzzyMatcher:
    """
    Fuzzy matcher za pronalaženje najboljih poklapanja između skrejpovanih proizvoda i baze.
    
    Koristi fuzzy string matching sa pragom od 95% sličnosti.
    """

    def __init__(self, model_to_match):
        self.model_to_match = model_to_match

    def match(self, scraped_products):
        """
        Pronalazi najbolja poklapanja između skrejpovanih proizvoda i komponenti u bazi.
        
        Za svaku komponentu u bazi pronalazi najbolje poklapanje među skejpovanim proizvodima.
        Koristi normalizovana imena i fuzzy matching sa pragom od 95%.
        
        :param scraped_products: Lista skejpovanih proizvoda
        :type scraped_products: list[ScrapedProduct]
        :return: Lista filtrirane komponente sa pronađenim poklapanjima
        :rtype: list[FuzzyFilteredProduct]
        """
        try:
            result=[]
            normalizer = NORMALIZERS[self.model_to_match]
            model = MODELS[self.model_to_match]
            components = model.objects.all()
            for comp in components:
                best = None
                score = 0
                for scrp in scraped_products:
                    s=fuzz.ratio(normalizer(scrp.name),normalizer(comp.component_ptr.name) )
                    #print(normalizer(scrp.name)+"   "+ normalizer(comp.component_ptr.name)+"   "+ str(s))
                    if s > score:
                        score = s
                        best = scrp
                if best is None:
                    continue
                if score < 88:
                    continue

                result.append(FuzzyFilteredProduct(
                    id=comp.component_ptr.id,
                    price=best.price,
                    shop=best.shop,
                    url=best.url
                ))
            return result
        except Exception as e:
            print(e)
            return []