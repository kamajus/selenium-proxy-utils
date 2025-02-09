import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from plugin import add_proxy
from plugin.schemas import Proxy


def test_plugin(proxy):
    browser_options = webdriver.ChromeOptions()
    browser_options.add_argument("--disable-logging")
    browser_options.add_argument("--log-level=3")
    browser_options.add_argument("--disable-infobars")
    browser_options.add_argument("--headless")

    add_proxy(browser_options, proxy=Proxy(**proxy))

    driver = webdriver.Chrome(browser_options)
    driver.get("https://apip.cc/json")

    time.sleep(10)

    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), '{proxy['host']}')]")
    except NoSuchElementException:
        raise Exception("Proxy not working!")
    finally:
        driver.quit()
