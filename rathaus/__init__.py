import re

import parsel
import requests


class RathausBoothScraper:

    MARKET_NAME = 'Rathaus'

    BOOTHS_URL = 'https://www.weihnachtsmarkt-muenster.com/de/aussteller/'

    @property
    def booths(self):
        if not hasattr(self, '_booths'):
            self._booths = dict(self.scrape_booths())
        return self._booths

    def fetch_booth(self, booth_id):
        return self.booths[booth_id]

    def scrape_booths(self):
        response = requests.get(self.BOOTHS_URL)
        response.raise_for_status()
        sel = parsel.Selector(response.text)
        for booth_sel in sel.css('tr.exhibitor-row'):
            booth_id = int(booth_sel.css(
                '::attr(data-booth-number)').extract_first())
            # Super unnecessary dark magic to collect data from all parse_xyz
            # methods
            data = {
                attr[len('parse_'):]: getattr(self, attr)(booth_sel)
                for attr in dir(self)
                if attr.startswith('parse_')
            }
            yield booth_id, data

    def parse_market(self, booth_sel):
        return self.MARKET_NAME

    def parse_owner(self, booth_sel):
        contact_data = {}
        for link in booth_sel.css('td.contact > a::attr(href)').extract():
            if link.startswith('http'):
                contact_data['web_url'] = link
            elif link.startswith('tel:'):
                contact_data['telephone'] = link.split(':', 1)[1]
            else:
                raise ValueError("Unexpected contact link: %s" % link)
        return contact_data

    def _get_text(self, booth_sel, td_class):
        text = '\n'.join(
            x.strip() for x in booth_sel.css(f'td.{td_class}::text').extract()
            if x.strip())
        text = text.replace('<br>', '\n')
        assert '<' not in text, '"{text}" contains unexpected HTML tags'
        return text

    def parse_name(self, booth_sel):
        return self._get_text(booth_sel, 'name').splitlines()[0]

    def parse_description(self, booth_sel):
        try:
            return self._get_text(booth_sel, 'name').split('\n', 1)[1]
        except IndexError:
            return None

    def parse_type(self, booth_sel):
        return self.parse_tags(booth_sel)[0]

    def parse_tags(self, booth_sel):
        BLACKLIST = ['sonstiges']
        return [
            x for x in
            self._get_text(booth_sel, 'category').split(' / ')
            if x.lower() not in BLACKLIST
        ]

    def parse_goods(self, booth_sel):
        BLACKLIST = ['mehr']
        return [
            x.strip()
            for x in re.split(
                # Match ',', '&', ' und', and ' u.'
                r'(?:[,&]|\s+u(?:nd|\.))',
                self.parse_description(booth_sel) or '')
            if x.strip() and x.strip().lower() not in BLACKLIST
        ]
