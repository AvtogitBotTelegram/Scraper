import logging
import random
import time

from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from scraper.api.client import client
from scraper.bag import Bag
from scraper.config import config


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def random_time():
    return random.choice((range(3, 8)))


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
        time.sleep(random_time())

        driver.find_element(By.CLASS_NAME, 'lk2gmii').click()
        time.sleep(random_time())

        login_input = driver.find_element(By.ID, 'signInLoginInput')
        login_input.clear()
        login_input.send_keys(config.login_emex)
        time.sleep(random_time())

        password_input = driver.find_element(By.ID, 'signInPasswordInput')
        password_input.clear()
        password_input.send_keys(config.password_emex)
        time.sleep(random_time())

        driver.find_element(By.CLASS_NAME, 'l1iy1epa').click()
        time.sleep(random_time())

        driver.find_element(By.CLASS_NAME, 'l-inmotion').click()
        time.sleep(random_time())

        bag = Bag(driver)

        request = bag.request(driver)
        cookies = bag.cookies(driver)
        headers = bag.headers(request)
        body = bag.edit_request(request, {'countOnPage': 100})

        response_all = []

        response = client.emex.get_orders(headers=headers, request=body, cookies=cookies)
        response_all.append(response)
        time.sleep(random_time())
        for page in range(2, response_all[0]['PagesCount'] + 1):
            body = bag.edit_request(request, {'page': page, 'countOnPage': 100})
            response = client.emex.get_orders(headers=headers, request=body, cookies=cookies)
            response_all.append(response)
            time.sleep(random_time())

        driver.quit()

    except Exception as ex:
        logger.warning(ex)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
