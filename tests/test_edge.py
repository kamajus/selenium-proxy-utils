import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_proxy import add_proxy
from selenium_proxy.schemas import Proxy


def test_plugin(proxy):
    browser_options = webdriver.EdgeOptions()
    browser_options.add_argument("headless")

    add_proxy(browser_options, proxy=Proxy(**proxy))

    driver = webdriver.Edge(browser_options)
    driver.get("https://apip.cc/json")

    time.sleep(10)

    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), '{proxy['host']}')]")
    except NoSuchElementException:
        raise Exception("Proxy not working!")
    finally:
        driver.quit()
