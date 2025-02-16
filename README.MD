# Selenium Proxy

A simple library to facilitate the use of proxies with Selenium and Python.

## Installation

```sh
pip install selenium-proxy-utils
```

## Usage

```python
from selenium import webdriver
from selenium_proxy import add_proxy
from selenium_proxy.schemas import Proxy

# Define browser options
browser_options = webdriver.ChromeOptions()
browser_options.add_argument("--disable-logging")
browser_options.add_argument("--log-level=3")
browser_options.add_argument("--disable-infobars")

# Define proxy settings
proxy = {
    "host": "proxy_address",
    "port": 8000,
    "username": "user",
    "password": "password"
}

# Add proxy settings (supports authenticated proxies)
add_proxy(browser_options, proxy=Proxy(**proxy))

# Initialize WebDriver
driver = webdriver.Chrome(options=browser_options)
driver.get("https://google.com")

# Keep the browser open for 120 seconds
import time
time.sleep(120)

# Close the browser
driver.quit()
```

## Requirements
- Python 3.x
- Selenium

## License
This project is licensed under the MIT License.
