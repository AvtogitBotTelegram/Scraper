from seleniumwire import webdriver
from seleniumwire.request import Request

from scraper.config import config


class Bag:

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def _to_bytes(self, body: dict) -> bytes:
        body_list = []
        for key, value in body.items():
            body_list.append(f'{key}={value}')
        return '&'.join(body_list)

    def _to_dict(self, request: Request) -> dict:
        body = request.body.decode('utf-8').split('&')
        req = {}
        for i in body:
            a = i.split('=')
            if len(a) == 2:
                req[a[0]] = a[1]
            else:
                req[a[0]] = ''
        req['countOnPage'] = 100
        return req

    def edit_request(self, body: Request, params: dict):
        request = self._to_dict(body)
        for key, value in params.items():
            request[key] = value
        return self._to_bytes(request)

    def cookies(self, driver: webdriver) -> dict:
        cookies = driver.get_cookies()
        cookie = {c['name']: c['value'] for c in cookies}
        return cookie

    def headers(self, response: Request) -> dict:
        headers = {}
        payload = response.headers._headers
        for header in payload:
            headers[header[0]] = header[1]
        del headers['Content-Length']
        return headers

    def request(self, driver: webdriver) -> Request:
        for requst in driver.requests:
            if requst.url == config.api_order:
                return requst
