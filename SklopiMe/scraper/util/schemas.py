#Aleksandar Cvetkovic 2023/0150
from dataclasses import dataclass


@dataclass
class ScrapedProduct:
    """
    Šema za skrejpovani proizvod sa veb-sajta.
    
    Sadrži osnovne informacije o proizvodu prikupljene skrejperom.
    """
    name: str  #: Naziv proizvoda
    price: int  #: Cena proizvoda u RSD
    url: str  #: URL link do proizvoda
    shop: str  #: Naziv prodavnice

@dataclass
class FuzzyFilteredProduct:
    """
    Šema za filtrirani proizvod nakon fuzzy matchinga.
    
    Predstavlja povezanost između skrejpovanog proizvoda i komponente iz baze podataka.
    """
    id: int  #: ID komponente iz baze podataka
    price: int  #: Cena proizvoda u RSD
    url: str  #: URL link do proizvoda
    shop: str  #: Naziv prodavnice