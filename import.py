import json

from utils import BoothPoster
from lamberti.lamberti import Lamberti

lamberti = Lamberti()

post_helper = BoothPoster('http://localhost:8888/v1/buckets/weihnachtsmarkt/collections/booths/records',
                          ('admin', 'SUPER-SECURE-PASSWORD'))

with open('weihnachtsmaerkte_all.geojson') as geojsonfile:
    geojsondata = json.load(geojsonfile)

for booth_geometry in geojsondata["features"]:
    geometry = booth_geometry["geometry"]
    booth_no = int(booth_geometry["properties"]["STAND_NR"])

    # lamberti
    if booth_geometry["properties"]["NAME"] == "WH3":
        booth = lamberti.fetch_booth(booth_no)
        booth["geometry"] = geometry
        post_helper.post(booth)

    print(f'done processing {booth_geometry["properties"]["SCHLUESSEL"]}')
