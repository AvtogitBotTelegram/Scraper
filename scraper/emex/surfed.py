import random
import time

from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from scraper.config import config


class Surfed:

    def __init__(self) -> None:
        self.chromedriver = config.chromedriver
        self.user_agent = config.user_agent
        self.password_emex = config.password_emex
        self.login_emex = config.login_emex
        self.password_proxy = config.password_proxy
        self.login_proxy = config.login_proxy
        self.port_proxy = config.port_proxy
        self.host_proxy = config.host_proxy
        self.url_host = config.url_host

    def timeout(self):
        time.sleep(random.choice((range(3, 8))))

    def setting(self):
        options = webdriver.ChromeOptions()
        options.add_argument(self.user_agent)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        options.add_argument("window-size=1200x600")
        return options

    def proxy(self) -> dict[str, dict[str, str]]:
        proxy_options = {
            'proxy': {
                'http': f'http://{self.login_proxy}:{self.password_proxy}@{self.host_proxy}:{self.port_proxy}'
            }
        }
        return proxy_options

    def sign_in(self, driver):
        driver.get(config.url_host)
        self.timeout()

    def login(self, driver):
        driver.find_element(By.CLASS_NAME, 'lk2gmii').click()
        self.timeout()
        login_input = driver.find_element(By.ID, 'signInLoginInput')
        login_input.clear()
        login_input.send_keys(config.login_emex)
        self.timeout()
        password_input = driver.find_element(By.ID, 'signInPasswordInput')
        password_input.clear()
        password_input.send_keys(config.password_emex)
        self.timeout()
        driver.find_element(By.CLASS_NAME, 'l1iy1epa').click()
        self.timeout()

    def enter_orders(self, driver):
        driver.find_element(By.CLASS_NAME, 'l-inmotion').click()
        self.timeout()

    def go(self):
        driver = webdriver.Chrome(
            self.chromedriver,
            options=self.setting(),
            seleniumwire_options=self.proxy())

        self.sign_in(driver)
        self.login(driver)
        self.enter_orders(driver)

        return driver
