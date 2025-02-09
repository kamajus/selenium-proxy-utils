from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.edge.options import Options as OptionsEdge

from selenium_proxy.exceptions import BrowserNotSupported
from selenium_proxy.schemas import Proxy
from selenium_proxy.webdriver import Chrome, Edge


def add_proxy(browser_options, proxy: Proxy):
    if isinstance(browser_options, OptionsChrome):
        chrome = Chrome(
            host=proxy.host, port=proxy.port, user=proxy.user, password=proxy.password
        )

        chrome.run(browser_options)
    elif isinstance(browser_options, OptionsEdge):
        edge = Edge(
            host=proxy.host, port=proxy.port, user=proxy.user, password=proxy.password
        )

        edge.run(browser_options)
    else:
        raise BrowserNotSupported()
