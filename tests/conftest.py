import random

import pytest
import requests

from selenium_proxy.schemas import Proxy


def get_proxies() -> dict:
    """Fetches a proxy from the external API and returns it."""
    try:
        response = requests.get(
            "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/https/data.json"
        )
        response.raise_for_status()
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching proxies: {e}")
    except ValueError as e:
        raise RuntimeError(f"Invalid data from proxy API: {e}")


def test_proxy(proxy: Proxy):
    try:
        proxy_dict = {
            "http": f"{proxy['ip']}:{proxy['port']}",
            "https": f"{proxy['ip']}:{proxy['port']}",
        }
        print(proxy_dict)

        response = requests.get("https://apip.cc/json", proxies=proxy_dict, timeout=5)
        response.raise_for_status()
        return proxy
    except requests.exceptions.RequestException:
        return None


@pytest.fixture
def proxy():
    proxies = get_proxies()
    proxy = None

    if not proxies:
        return None

    while proxies:
        proxy = random.choice(proxies)
        result = test_proxy(proxy)
        if result:
            proxy = result
            break
        else:
            proxies.remove(proxy)

    proxy["host"] = proxy["ip"]
    return proxy
