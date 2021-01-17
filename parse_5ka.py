import requests
import json
import time
from pathlib import Path


class ParseError(Exception):
    def __init__(self, txt):
        self.txt = txt

class Parse5ka:
    _params = {
        'records_per_page': 100,
        'page': 1,
    }
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    def __init__(self, start_url):
        self.start_url = start_url

    def parse(self, url):
        if not url:
            url = self.start_url
        params = self._params
        while url:
            response = self.__get_response(url, params=params, headers=self._headers)
            if params:
                params = {}
            data = json.loads(response.text)
            url = data.get('next')

            yield data.get('results')

    @staticmethod
    def __get_response(url, *args, **kwargs) -> requests.Response:
        while True:
            try:
                response = requests.get(url, *args, **kwargs)
                if response.status_code > 399:
                    raise ParseError(response.status_code)
                time.sleep(0.1)
                return response

            except(requests.RequestException, ParseError):
                time.sleep(0.5)
                continue

    def run(self):
        for products in self.parse(self.start_url):
            for product in products:
                self.save(product, product["id"])

    @staticmethod
    def save(data: dict, file_name):
        with open(f"products/{file_name}.json", "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False)

        print(1)


class ParserCatalog(Parse5ka):
    def __init__(self, start_url, category_url):
        self.category_url = category_url
        super().__init__(start_url)

    def get_categories(self, url):
        response = requests.get(url, headers=self._headers)
        return response.json()

    def run(self):
        for category in self.get_categories(self.category_url):
            data = {
                "name": category["parent_group_name"],
                "code": category["parent_group_code"],
                "products": [],
            }

            self._params["categories"] = category["parent_group_code"]

            for products in self.parse(self.start_url):
                data["products"].extend(products)
            self.save(data, category["parent_group_code"])


if __name__ == "__main__":
    parser = ParserCatalog(
        "https://5ka.ru/api/v2/special_offers/", "https://5ka.ru/api/v2/categories/"
    )
    parser.run()