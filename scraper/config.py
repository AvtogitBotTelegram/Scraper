import os
from dataclasses import dataclass


@dataclass
class Config:

    execute_now: str

    login_proxy: str
    password_proxy: str
    host_proxy: str
    port_proxy: str

    url_host: str
    chromedriver: str

    login_emex: str
    password_emex: str

    api_order: str
    api_avtogit: str
    user_agent: str


config = Config(
    execute_now=os.environ['EXECUTE_NOW'],
    login_proxy=os.environ['LOGIN_PROXY'],
    password_proxy=os.environ['PASSWORD_PROXY'],
    host_proxy=os.environ['HOST_PROXY'],
    port_proxy=os.environ['PORT_PROXY'],
    url_host=os.environ['URL_HOST'],
    chromedriver=os.environ['CHROMEDRIVER'],
    login_emex=os.environ['LOGIN_EMEX'],
    password_emex=os.environ['PASSWORD_EMEX'],
    api_order=os.environ['API_ORDER'],
    api_avtogit=os.environ['API_AVTOGIT'],
    user_agent=os.environ['USER_AGENT'],
)
