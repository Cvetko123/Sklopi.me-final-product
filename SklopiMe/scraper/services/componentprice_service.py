#Aleksandar Cvetkovic 2023/0150
from app.models import Componentprice, Component


class ComponentService:
    """
    Servis za upravljanje cenama komponenti.
    
    Čuva i ažurira cene komponenti iz različitih prodavnica u bazi podataka.
    """

    def save(self, filtered_product):
        """
        Čuva ili ažurira cenu komponente u bazi podataka.
        
        Ako cena za komponentu iz određene prodavnice već postoji, ažurira se.
        Ako ne postoji, kreira se nova.
        
        :param filtered_product: Objekt sa informacijama o proizvodu (id, price, url, shop)
        :type filtered_product: FuzzyFilteredProduct
        """
        component = Component.objects.get(id=filtered_product.id)
        Componentprice.objects.update_or_create(
            idcomponent=component,
            shopname=filtered_product.shop,
            defaults={
                "price": filtered_product.price,
                "link": filtered_product.url
            }
        )