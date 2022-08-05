import logging
import random
import time
import traceback
import orjson

from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from scraper.api.client import client
from scraper.bag import Bag
from scraper.config import config
from scraper.api.schemas import Order


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

        response_all: list[Order] = []
        pages = client.emex.get_orders(headers=headers, request=body, cookies=cookies)['PagesCount']
        time.sleep(random_time())
        for page in range(1, pages + 1):
            body = bag.edit_request(request, {'page': page, 'countOnPage': 100})
            responses = client.emex.get_orders(headers=headers, request=body, cookies=cookies)

            for response in responses['Rows']:
                response_all.append(Order(
                    globalId=int(response['GlobalId']),
                    order_date=str(response['POrdDate']),
                    delivery_type=str(response['DeliveryRegionType']),
                    client_logo=str(response['ClientUserLogo']),
                    client_name=str(response['ClientUserName']),
                    client_full_name=str(response['ClientSort']),
                    detail_num=str(response['DetailNum']),
                    detail_label=str(response['DetailLabel']),
                    sum_value=int(response['SumValue']),
                    sum_profit=int(response['SumProfitValue']),
                    return_data=str(response['ReturnBoundDate']),
                    return_data_shipping=str(response['ReturnShippingEndDate']),
                    status_shipping=str(response['Statuses'][0]['Title']),
                    arrival_date=str(response['Statuses'][0]['StatusInfo']['Date']),
                ))
            time.sleep(random_time())

        json_response = orjson.dumps([Order.from_orm(order).dict() for order in response_all])
        client.avtogit.send_orders(json_response)

        driver.quit()

    except Exception as ex:
        logger.warning(ex, traceback.format_exc())
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
