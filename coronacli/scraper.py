import requests

from abc import ABC, abstractmethod
from collections import OrderedDict

from coronacli.config import OWID_DATA_URL


class BaseScraper(ABC):
    """ Abstract scraper class defining common functionality among all scrapers and abstract methods to implement """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_data(url):
        """ Submits HTTP GET request to extract data from given url

        :param url - an HTTP URL to submit the request to
        :returns the result of the GET request
        """
        # TODO add exception handling/retries
        return requests.get(url)

    @staticmethod
    def get_text(request_data):
        """ Given a result from some request to a URL, this method extracts the relevant site text from it

        :param request_data - the data returned from a request such as request.get
        :returns the text contained within that result
        """
        return request_data.text

    @abstractmethod
    def _extract_data(self, data_dict):
        pass

    @abstractmethod
    def scrape(self, url):
        pass


class OurWorldInDataScraper(BaseScraper):
    """ Extracts country information and COVID-19 cases by country from
    https://github.com/owid/covid-19-data/tree/master/public/data

    Parses these data by splitting the information into two distinct collections to pass downstream
    """
    def __init__(self):
        self.owid_covid_data = {}
        self.owid_country_data = {}
        super().__init__()

    def _extract_countries_object(self, country_code, country_obj):
        country_obj.pop("data")
        country_obj["country_code"] = country_code
        self.owid_country_data[country_code] = country_obj

    def _extract_covid_object(self, country_code, country_obj):
        covid_data = country_obj["data"]
        self.owid_covid_data[country_code] = covid_data

    def _extract_data(self, data_dict):
        for country_code, country_obj in data_dict.items():
            self._extract_covid_object(country_code, country_obj)
            self._extract_countries_object(country_code, country_obj)

    def scrape(self, url=OWID_DATA_URL):
        """ Performs the necessary calls to request data from given URL, parse it, and extract the relevant items

        :param url - the URL which contains the Our World In Data COVID-19 dataset (defaults to config)
        :returns data on COVID-19 cases and country information from OWID dataset
        """
        import json
        # Get the JSON string from the given URL and parse into Python dictionary
        data = self.get_data(url)
        data_text = self.get_text(data)
        data_dict = json.loads(data_text, object_pairs_hook=OrderedDict)
        # Parse the resulting dictionary obtained from the JSON at given URL
        self._extract_data(data_dict)
        return self.owid_covid_data, self.owid_country_data


def get_scraper(name):
    """ Returns the relevant class by the given name ala factory pattern

    :param name - the name of the scraper to return
    :returns the relevant scraper class for the given scraper name
    """
    supported_scrapers = {"OurWorldInData": OurWorldInDataScraper}
    try:
        scraper_object = supported_scrapers[name]
    except KeyError:
        raise KeyError("{0} is not a supported scraper".format(name))
    return scraper_object
