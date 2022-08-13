import logging
import random
import time
import traceback

import orjson

from scraper.api.client import client
from scraper.api.schemas import Order
from scraper.config import config
from scraper.emex.bag import Bag
from scraper.emex.surfed import Surfed

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def timeout():
    time.sleep(random.choice((range(6, 13))))


def convert(order):
    return Order(
        globalId=int(order['GlobalId']),
        order_date=str(order['POrdDate']),
        delivery_type=str(order['DeliveryRegionType']),
        client_logo=str(order['ClientUserLogo']),
        client_name=str(order['ClientUserName']),
        client_full_name=str(order['ClientSort']),
        detail_num=str(order['DetailNum']),
        detail_label=str(order['DetailLabel']),
        sum_value=int(order['SumValue']),
        sum_profit=int(order['SumProfitValue']),
        return_data=str(order['ReturnBoundDate']),
        return_data_shipping=str(order['ReturnShippingEndDate']),
        status_shipping=str(order['Statuses'][0]['Title']),
        arrival_date=str(order['Statuses'][0]['StatusInfo']['Date']),
    )


def parse_orders_page(headers, cookies, request, body, bag):
    response_all: list[Order] = []
    response = client.emex.get_orders(headers=headers, request=body, cookies=cookies)
    timeout()

    pages: int = response['PagesCount']
    for page in range(1, pages + 1):
        body = bag.edit_request(request, {'page': page, 'countOnPage': '100'})
        responses = client.emex.get_orders(headers=headers, request=body, cookies=cookies)
        timeout()

        for order in responses['Rows']:
            response_all.append(convert(order))

    return response_all


def main():
    try:
        surfed = Surfed(config)
        driver = surfed.go()

        bag = Bag(driver)
        request = bag.request()
        cookies = bag.cookies()
        headers = bag.headers()
        body = bag.edit_request(request, {'countOnPage': '100'})
        driver.quit()

        orders = parse_orders_page(
            headers=headers,
            cookies=cookies,
            body=body,
            request=request,
            bag=bag,
        )

        json_response = orjson.dumps([Order.from_orm(order).dict() for order in orders])
        client.avtogit.send_orders(json_response)

    except Exception as ex:
        logger.warning(ex, traceback.format_exc())
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
