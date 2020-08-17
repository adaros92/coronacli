import requests

from abc import ABC, abstractmethod
from collections import OrderedDict

from coronacli.config import OWID_DATA_URL


class BaseScraper(ABC):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_data(url):
        # TODO add exception handling/retries
        return requests.get(url)

    @staticmethod
    def get_text(request_data):
        return request_data.text

    @abstractmethod
    def _extract_data(self, data_dict):
        pass

    @abstractmethod
    def scrape(self, url):
        pass


class OurWorldInDataScraper(BaseScraper):

    def __init__(self):
        self.owid_covid_data = {}
        self.owid_country_data = {}
        super().__init__()

    def _extract_countries_object(self, country_code, country_obj):
        country_obj.pop("data")
        country_obj["country_code"] = country_code
        self.owid_country_data[country_code] = country_obj

    def _extract_covid_object(self, country_code, country_obj):
        covid_data = country_obj["data"][0]
        self.owid_covid_data[country_code] = covid_data

    def _extract_data(self, data_dict):
        for country_code, country_obj in data_dict.items():
            self._extract_covid_object(country_code, country_obj)
            self._extract_countries_object(country_code, country_obj)

    def scrape(self, url=OWID_DATA_URL):
        import json

        data = self.get_data(url)
        data_text = self.get_text(data)
        data_dict = json.loads(data_text, object_pairs_hook=OrderedDict)

        self._extract_data(data_dict)

        return self.owid_covid_data, self.owid_country_data


def get_scraper(name):
    supported_scrapers = {"OurWorldInData": OurWorldInDataScraper}
    try:
        scraper_object = supported_scrapers[name]
    except KeyError:
        raise KeyError("{0} is not a supported scraper".format(name))
    return scraper_object
