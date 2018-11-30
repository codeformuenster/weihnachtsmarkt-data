import requests
import json
import os
from parsel import Selector


class Lamberti:
    def __init__(self):
        with open(os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__), 'lamberti.json'))) as jsonfile:
            self.booths = json.load(jsonfile)

    def fetch_booth(self, booth_number):
        booth = next(b for b in self.booths if b['nr'] == booth_number)

        r = requests.get(booth['url'])
        r.raise_for_status()
        if r.status_code == 200:
            text = r.text
            selector = Selector(text=text)

            booth_name = selector.css('.booth-title::text').get()
            booth_descr = selector.css('.booth-body > p::text').getall()

            if isinstance(booth_descr, list):
                booth_descr = " ".join(booth_descr)

            booth_owner_company = selector.css(
                '.contactParticle--company::text').get()
            booth_owner_name = selector.css(
                '.contactParticle--name\:firstname\,lastname::text').get()
            booth_owner_street = selector.css(
                '.contactParticle--street::text').get()
            booth_owner_city = selector.css(
                '.contactParticle--city\:postal_code\,locality::text').get()
            booth_owner_phone = selector.css(
                '.contactParticle--phone::text').get()
            booth_owner_email = selector.css(
                '.contactParticle--email > a::text').get()
            booth_owner_web_url = selector.css(
                '.contactParticle--website > a::attr(href)').get()

            booth_products = selector.css(".products::text").get()
            if booth_products:
                booth_products = booth_products.split(",")
                booth_products = list(
                    map(lambda b: {"name": b.strip()}, booth_products))
            else:
                booth_products = []

            booth_owner = ", ".join([elem.strip() if elem is not None else ''
                                     for elem in [booth_owner_name, booth_owner_company,
                                                  booth_owner_street, booth_owner_city]])
        else:
            booth_name = 'Unbekannt'
            booth_owner = 'Unbekannt'

        return {
            "owner": {
                "name": booth_owner,
                "email": booth_owner_email,
                "web_url": booth_owner_web_url,
                "telephone": booth_owner_phone
            },
            "name": booth_name,
            "tags": [
                "Ohne",
            ],
            "type": "food",
            "market": "Lamberti",
            "goods": booth_products,
            "description": booth_descr,
        }
