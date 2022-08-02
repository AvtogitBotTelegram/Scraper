import time
import httpx
import json
import logging

from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from seleniumwire.request import Request

from scraper.config import config

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def _to_bytes(body: dict) -> bytes:
    body_list = []
    for key, value in body.items():
        body_list.append(f'{key}={value}')
    return '&'.join(body_list)


def _to_dict(request: Request) -> dict:
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


def _get_cookies(driver: webdriver) -> dict:
    cookies = driver.get_cookies()
    cookie = {c['name']: c['value'] for c in cookies}
    return cookie


def _get_headers(response: Request) -> dict:
    headers = {}
    payload = response.headers._headers
    for header in payload:
        headers[header[0]] = header[1]
    del headers['Content-Length']
    return headers


def _get_request(driver: webdriver) -> Request:
    for requst in driver.requests:
        if requst.url == config.api_order:
            return requst


def main():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(config.user_agent)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        options.add_argument("window-size=1200x600")
        proxy_options = {
            'proxy': {
                'http': f'http://{config.login_proxy}:{config.password_proxy}@{config.host_proxy}:{config.port_proxy}'
            }
        }

        driver = webdriver.Chrome(config.chromedriver, options=options, seleniumwire_options=proxy_options)

        driver.get(config.url_host)
        time.sleep(3)
        logging.debug('Зашеш на сайт emex')
        driver.maximize_window()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, 'lk2gmii').click()
        time.sleep(4)
        login_input = driver.find_element(By.ID, 'signInLoginInput')
        login_input.clear()
        login_input.send_keys(config.login_emex)
        time.sleep(2)
        password_input = driver.find_element(By.ID, 'signInPasswordInput')
        password_input.clear()
        password_input.send_keys(config.password_emex)
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'l1iy1epa').click()
        logging.debug('ВоВеВв систему')
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'l-inmotion').click()
        logging.debug('ВаВеВ в заказы')
        time.sleep(5)

        request = _get_request(driver)
        cookies = _get_cookies(driver)
        headers = _get_headers(request)
        body = _to_dict(request)
        req = _to_bytes(body)

        response_all = []

        response = httpx.post(config.api_order, headers=headers, data=req, cookies=cookies)
        response_all.append(json.loads(response.content))
        time.sleep(4)
        for page in range(2, response_all[0]['PagesCount'] + 1):
            body = _to_dict(request)
            body['page'] = page
            req = _to_bytes(body)
            response = httpx.post(config.api_order, headers=headers, data=req, cookies=cookies)
            response_all.append(json.loads(response.content))
            time.sleep(5)

        driver.quit()

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
