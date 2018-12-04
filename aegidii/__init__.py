import re

import requests
import json


class Aegidii:
    MARKET_NAME = 'Aegidii'
    BOOTHS_URL = 'https://www.aegidii-weihnachtsmarkt.de/'

    def fetch_booths(self):
        r = requests.get('https://www.aegidii-weihnachtsmarkt.de/wp-json/wp/v2/posts?_embed&per_page=100')

        if r.status_code == 200:
            results = []
            data = r.json()
            for row in data:
                booth = self.fetch_booth(row)
                results.append(booth)

    def fetch_booth(self, row):
        link = row['link']
        name = row['title']['rendered']

        content = row['content']['rendered']
        description = re.match(".*\[vc_column_text\](.*)\[\/vc_column_text\]", content)
        if description is not None:
            description = description.group(1)
        else:
            description = ""

        tag = re.match(".*\[vc_custom_heading text=&#8220;(.*)&#8220; font_container=&#8220;", content)
        if tag is not None:
            tag = tag.group(1)
        else:
            tag = "Ohne"

        return {
            "owner": {
                "name": "",
                "email": "",
                "web_url": link,
                "telephone": ""
            },
            "name": name,
            "tags": [
                tag,
            ],
            "type": "food",
            "market": self.MARKET_NAME,
            "goods": "",
            "description": description,
        }
