import random
import time

from selenium.webdriver.common.by import By
from seleniumwire import webdriver


class Surfed:

    def __init__(self, config) -> None:
        self.config = config

    def timeout(self):
        time.sleep(random.choice((range(3, 8))))

    def setting(self):
        options = webdriver.ChromeOptions()
        options.add_argument(self.config.user_agent)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        options.add_argument("window-size=1200x600")
        return options

    def proxy(self) -> dict[str, dict[str, str]]:
        proxy_options = {
            'proxy': {
                'http': f'http://{self.config.login_proxy}:{self.config.password_proxy}@{self.config.host_proxy}:{self.config.port_proxy}'
            }
        }
        return proxy_options

    def sign_in(self, driver):
        driver.get(self.config.url_host)
        self.timeout()

    def login(self, driver):
        driver.find_element(By.CLASS_NAME, 'lk2gmii').click()
        self.timeout()
        login_input = driver.find_element(By.ID, 'signInLoginInput')
        login_input.clear()
        login_input.send_keys(self.config.login_emex)
        self.timeout()
        password_input = driver.find_element(By.ID, 'signInPasswordInput')
        password_input.clear()
        password_input.send_keys(self.config.password_emex)
        self.timeout()
        driver.find_element(By.CLASS_NAME, 'l1iy1epa').click()
        self.timeout()

    def enter_orders(self, driver):
        driver.find_element(By.CLASS_NAME, 'l-inmotion').click()
        self.timeout()

    def go(self):
        driver = webdriver.Chrome(
            self.config.chromedriver,
            options=self.setting(),
            seleniumwire_options=self.proxy())

        self.sign_in(driver)
        self.login(driver)
        self.enter_orders(driver)

        return driver
