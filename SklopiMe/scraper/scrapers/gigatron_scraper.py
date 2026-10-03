#Aleksandar Cvetkovic 2023/0150

from playwright.sync_api import sync_playwright
from scraper.scrapers.base_scraper import BaseScraper
from scraper.util.schemas import ScrapedProduct


class GigatronScraper(BaseScraper):
    """
    Skrejper za Gigatron veb-sajt.
    
    Prikuplja podatke o računarskim komponentama sa Gigatron-a kroz automatizovani pregledač koristeći Playwright.
    """

    STORE_NAME = "Gigatron"

    def scrape(self):
        """
        Skrejpuje proizvode sa Gigatron-a.
        
        Navigira kroz sve stranice rezultata, ekstraktuje naziv, cenu i URL za svaki proizvod
        i vraća listu skrejpovanih proizvoda.
        
        :return: Lista ScrapedProduct objekata sa podacima o proizvodima
        :rtype: list[ScrapedProduct]
        """
        try:

            result = []

            with sync_playwright() as p:

                browser = p.chromium.launch(headless=True)
                page = browser.new_page()



                page.goto(self.url)

                while True:
                    #print("doing one page")

                    page.wait_for_selector('a[href^="/proizvod/"]')

                    products = page.query_selector_all('a[href^="/proizvod/"]')

                    for product in products:

                        name = product.inner_text().strip()

                        if name == "":
                            continue

                        price_element = product.query_selector(
                        'xpath=following::p[@itemprop="price"][1]'
                        )

                        price_text = price_element.inner_text().strip()

                        price = int(
                        price_text
                        .replace('RSD', '')
                        .replace('.', '')
                        .replace(',00', '')
                        .strip()
                        )

                        url = product.get_attribute('href')

                        result.append(
                            ScrapedProduct(
                                name=name,
                                price=price,
                                url="https://gigatron.rs" + url,
                                shop=self.STORE_NAME
                            )
                        )

                    next_button = page.locator(
                        'button[aria-label="Sledeća strana"]'
                    )

                    if next_button.count() == 0:
                        #print("no more products 1")
                        break

                    if not next_button.is_enabled():
                        #print("no more products 2")
                        break

                    next_button.click()

                    page.wait_for_load_state("networkidle")


                browser.close()

            return result

        except Exception as e:
            print(e)
            return []