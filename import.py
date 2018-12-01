import json
import os
from kinto_http import Client

from utils import AccountsHelper, del_none

from lamberti.lamberti import Lamberti
from rathaus import RathausBoothScraper


SCRAPERS = {
    'WH1': RathausBoothScraper(),
    'WH3': Lamberti(),
}

kinto_url = os.getenv('KINTO_URL', "http://localhost:8888/v1")
kinto_user = os.getenv('KINTO_USER', "admin")
kinto_password = os.getenv('KINTO_PASSWORD', "SUPER-SECURE-PASSWORD")

accounts_helper = AccountsHelper(server_url=kinto_url,
                                 auth=(kinto_user, kinto_password))


def create_booth_with_auth(booth, username):
    password = accounts_helper.create_user(username)
    print(f'created user "{username}" with password "{password}"')

    client = Client(server_url=kinto_url, auth=(username, password),
                    bucket="weihnachtsmarkt", collection="booths")

    del_none(booth)
    client.create_record(data=booth)
    print(f'created booth {booth["name"]} for market {booth["market"]}')


with open('weihnachtsmaerkte_all.geojson') as geojsonfile:
    geojsondata = json.load(geojsonfile)

for booth_geometry in geojsondata["features"]:
    geometry = booth_geometry["geometry"]
    try:
        booth_no = int(booth_geometry["properties"]["STAND_NR"])
    except ValueError:
        print(
            f'Skipping booth with number "{booth_geometry["properties"]["STAND_NR"]}"')
        continue
    booth_key = booth_geometry["properties"]["SCHLUESSEL"]
    market_id = booth_geometry["properties"]["NAME"]

    scraper = SCRAPERS.get(market_id)
    if not scraper:
        print(f'Unknown market {market_id}')
        continue
    booth = scraper.fetch_booth(booth_no)
    booth["geometry"] = geometry
    create_booth_with_auth(booth, booth_key)
