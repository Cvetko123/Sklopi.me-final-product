#Aleksandar Cvetkovic 2023/0150
from playwright.sync_api import sync_playwright
from scraper.scrapers.base_scraper import BaseScraper
from scraper.util.schemas import ScrapedProduct


class ComputerlandScraper(BaseScraper):
    """
    Skrejper za ComputerLand veb-sajt.
    
    Prikuplja podatke o računarskim komponentama sa ComputerLand-a kroz automatizovani pregledač koristeći Playwright.
    """

    STORE_NAME = "ComputerLand"

    def scrape(self):
        """
        Skrejpuje proizvode sa ComputerLand-a.
        
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

                    page.wait_for_selector('li.category-product')

                    products = page.query_selector_all('li.category-product')

                    for product in products:

                        name = product.get_attribute("data-name")
                        url = product.get_attribute("data-url")
                        price =product.get_attribute("data-price")

                        if not name or not url or not price:
                            continue


                        result.append(
                            ScrapedProduct(
                                name=name,
                                price=int(price),
                                url=url,
                                shop=self.STORE_NAME
                            )
                        )

                    next_button = page.locator(
                        'ul.pagination-shop a[aria-label="Next"]'
                    )

                    if next_button.count() == 0:
                        break

                    next_url = next_button.get_attribute("href")

                    if next_url is None:
                        break

                    page.goto(next_url)

                    page.wait_for_load_state("networkidle")


                browser.close()

            return result

        except Exception as e:
            print(e)
            return []