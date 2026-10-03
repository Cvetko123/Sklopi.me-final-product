"""
Modul za normalizaciju imena komponenti

**Opis:**

Sadrži funkcije za normalizaciju imena računarskih komponenti. Normalizacija uključuje
uklanjanje specifičnih detalja, znakova i irelevantnih reči kako bi se omogućilo
bolje fuzzy matching između imena iz različitih prodavnica i imena u bazi podataka.
"""
import re


def _normalize(name: str) -> str:
    """
    Osnovna normalizacija imena.
    
    Pretvara na velika slova, uklanja sadržaj u zagradama i suvišne razmake.
    
    :param name: Naziv koji se normalizuje
    :return: Normalizovani naziv
    """
    name = name.upper()
    name = re.sub(r"\(.*?\)", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()


def normalize_cpu_name(name):
    """
    Normalizuje naziv procesora.
    
    Uklanja: frekvenciju, socket tip, redundantne reči (CPU, BOX, OEM, itd.)
    
    :param name: Naziv procesora
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    name = re.sub(r'\d+(?:[.,]\d+)?\s*(?:GHZ|HZ)', '', name, flags=re.IGNORECASE)

    # remove sockets
    name = re.sub(r'\b(AM4|AM5|LGA\d+|1151|1200|1700|1851)\b', '', name)

    # remove packaging / irrelevant words
    remove_words = [
        "PROCESSOR",
        "PROCESOR",
        "CPU",
        "BOX",
        "TRAY",
        "MPK",
        "OEM",
        "RETAIL",
        "WITH",
        "COOLER",
        "WRAITH",
    ]

    for word in remove_words:
        name = re.sub(rf'\b{word}\b', '', name)

    # normalize Intel naming
    name = name.replace("INTEL CORE", "INTEL")
    name = name.replace("CORE ULTRA", "ULTRA")

    # remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def normalize_gpu_name(name):
    """
    Normalizuje naziv grafičke kartice.
    
    Uklanja: tip kartice, izdanje, RGB oznake, varijante hlađenja (OC, GAMING, WINDFORCE, itd.)
    
    :param name: Naziv grafičke kartice
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "GRAPHICS CARD",
        "GRAFICKA KARTA",
        "GPU",
        "OC EDITION",
        "OC",
        "GAMING",
        "DUAL",
        "TWIN",
        "TRIPLE",
        "WINDFORCE",
        "VENTUS",
        "EAGLE",
        "PHOENIX",
        "RGB",
        "LHR",
    ]

    for word in remove:
        name = name.replace(word, "")


    return re.sub(r"\s+", " ", name).strip()


def normalize_storage_name(name):
    """
    Normalizuje naziv memorijskog uređaja.
    
    Uklanja: tip (SSD, HDD, NVME), format (M.2, SATA), generaciju (GEN3, GEN4, GEN5), lokaciju (INTERNAL, EXTERNAL)
    
    :param name: Naziv memorijskog uređaja
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "SSD",
        "HDD",
        "NVME",
        "M.2",
        "SATA",
        "PCIE",
        "PCI-E",
        "GEN3",
        "GEN4",
        "GEN5",
        "INTERNAL",
        "EXTERNAL",
    ]

    for word in remove:
        name = name.replace(word, "")


    return re.sub(r"\s+", " ", name).strip()


def normalize_motherboard_name(name):
    """
    Normalizuje naziv matične ploče.
    
    Uklanja: tip ploče, tip memorije (DDR4, DDR5), faktor (ATX, MINI-ITX), socket, WiFi oznaku
    
    :param name: Naziv matične ploče
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "MOTHERBOARD",
        "MATIČNA PLOČA",
        "MATICNA PLOCA",
        "DDR4",
        "DDR5",
        "ATX",
        "MICROATX",
        "M-ATX",
        "MATX",
        "MINI-ITX",
        "ITX",
        "SOCKET",
        "WIFI",
        "WI-FI",
    ]

    for word in remove:
        name = name.replace(word, "")

    return re.sub(r"\s+", " ", name).strip()

def normalize_ram_name(name):
    """
    Normalizuje naziv RAM memorije.
    
    Uklanja: tip memorije (DDR3, DDR4, DDR5), format (DIMM, SO-DIMM), RGB oznaku, set informacije, frekvenciju, CAS latenciju
    
    :param name: Naziv RAM memorije
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "DDR3",
        "DDR4",
        "DDR5",
        "DIMM",
        "UDIMM",
        "SO-DIMM",
        "RGB",
        "MEMORY",
        "MEMORIJA",
        "RAM",
        "KIT",
    ]

    for word in remove:
        name = name.replace(word, "")


    # kits
    name = re.sub(r"\d+\s*[X×]\s*\d+", "", name)

    # frequency
    name = re.sub(r"\d+\s*MHZ", "", name)

    # CL timing
    name = re.sub(r"CL\d+", "", name)

    return re.sub(r"\s+", " ", name).strip()


def normalize_cooler_name(name):
    """
    Normalizuje naziv hlađenja za procesor.
    
    Uklanja: tip hlađenja (AIR, LIQUID, AIO), RGB oznake, PWM, veličinu radijatora
    
    :param name: Naziv hlađenja
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "CPU COOLER",
        "COOLER",
        "AIR COOLER",
        "LIQUID COOLER",
        "AIO",
        "RGB",
        "ARGB",
        "PWM",
    ]

    for word in remove:
        name = name.replace(word, "")

    # radiator size
    name = re.sub(r"\d+\s*MM", "", name)

    return re.sub(r"\s+", " ", name).strip()


def normalize_psu_name(name):
    """
    Normalizuje naziv napajanja.
    
    Uklanja: tip modularnosti, efikasnost (80 PLUS, GOLD, PLATINUM), snagu u vat
    
    :param name: Naziv napajanja
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "POWER SUPPLY",
        "NAPAJANJE",
        "PSU",
        "MODULAR",
        "FULL MODULAR",
        "SEMI MODULAR",
        "80 PLUS",
        "BRONZE",
        "SILVER",
        "GOLD",
        "PLATINUM",
        "TITANIUM",
    ]

    for word in remove:
        name = name.replace(word, "")

    # wattage
    name = re.sub(r"\d+\s*W", "", name)

    return re.sub(r"\s+", " ", name).strip()


def normalize_case_name(name):
    """
    Normalizuje naziv kućišta za računar.
    
    Uklanja: tip (MID TOWER, FULL TOWER, MINI TOWER), RGB oznake, faktor
    
    :param name: Naziv kućišta
    :return: Normalizovani naziv
    """
    name = _normalize(name)

    remove = [
        "CASE",
        "KUĆIŠTE",
        "KUCISTE",
        "MID TOWER",
        "FULL TOWER",
        "MINI TOWER",
        "RGB",
        "ARGB",
        "TEMPERED GLASS",
        "TG",
    ]

    for word in remove:
        name = name.replace(word, "")

    return re.sub(r"\s+", " ", name).strip()