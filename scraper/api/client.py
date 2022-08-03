import json

import httpx

from scraper.config import config


class ApiClient:

    def __init__(self) -> None:
        self.emex = Emex()


class Emex:

    def get_orders(self, headers: dict, request: bytes, cookies: dict):
        response = httpx.post(config.api_order, headers=headers, data=request, cookies=cookies)
        return json.loads(response.content)


client = ApiClient()
