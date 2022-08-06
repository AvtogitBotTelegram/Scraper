import json

import httpx

from scraper.config import config


class ApiClient:

    def __init__(self) -> None:
        self.emex = Emex(config.api_order)
        self.avtogit = Avtogit(config.api_avtogit)


class Avtogit:

    def __init__(self, url) -> None:
        self.url = url

    def send_orders(self, orders) -> None:
        response = httpx.post(self.url, data=orders)
        response.raise_for_status()


class Emex:

    def __init__(self, url) -> None:
        self.url = url

    def get_orders(self, headers: dict[str, str], request, cookies: dict[str, str]):
        response = httpx.post(self.url, headers=headers, data=request, cookies=cookies)
        return json.loads(response.content)


client = ApiClient()
