import json
import re
import os

import parsel
import requests


class AegidiiBoothScraper:

    MARKET_NAME = 'Aegidii'

    def __init__(self):
        urls_path = os.path.join(os.path.dirname(__file__), 'aegidii.json')
        with open(urls_path) as f:
            self.booth_urls = {x['id']: x['url'] for x in json.load(f)}

    def fetch_booth(self, booth_id):
        response = requests.get(self.booth_urls[booth_id])
        response.raise_for_status()
        sel = parsel.Selector(response.text)
        # Super unnecessary dark magic to collect data from all parse_xyz
        # methods
        return {
            attr[len('parse_'):]: getattr(self, attr)(sel)
            for attr in dir(self)
            if attr.startswith('parse_')
        }

    def _get_desc_sel(self, sel):
        return sel.xpath(
            '//div[h2[@class="vc_custom_heading"]]'
        ).css(
            'div.wpb_text_column',
        )

    def parse_market(self, sel):
        return self.MARKET_NAME

    def parse_owner(self, sel):
        contact_data = {}
        url = self._get_desc_sel(sel).css('a::attr(href)').extract_first()
        if url:
            contact_data['web_url'] = url
        return contact_data

    def parse_name(self, sel):
        return sel.css(
            'meta[property="og:title"]::attr(content)').extract_first()

    def parse_description(self, sel):
        crumbs = self._get_desc_sel(sel).css(':not(a)::text').extract()
        desc = ' '.join(x.strip() for x in crumbs if x.strip())
        desc = re.sub(r'\s+([\.,])', r'\1', desc)
        desc = re.sub(r'([\.,])[\.,]*', r'\1', desc)
        desc = re.sub(r'\s+', ' ', desc)
        return desc
