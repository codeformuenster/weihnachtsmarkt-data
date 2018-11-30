import json
from kinto_http import Client

from utils import AccountsHelper, del_none

from lamberti.lamberti import Lamberti

lamberti = Lamberti()

server_url = "http://localhost:8888/v1"


accounts_helper = AccountsHelper(server_url=server_url,
                                 auth=('admin', 'SUPER-SECURE-PASSWORD'))


def create_booth_with_auth(booth, username):
    password = accounts_helper.create_user(username)
    print(f'created user "{username}" with password "{password}"')

    client = Client(server_url=server_url, auth=(username, password),
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

    # lamberti
    if market_id == "WH3":
        print('Lamberti:')
        booth = lamberti.fetch_booth(booth_no)
        booth["geometry"] = geometry
        create_booth_with_auth(booth, booth_key)
    else:
        print(f'Unknown market {booth_geometry["properties"]["NAME"]}')
