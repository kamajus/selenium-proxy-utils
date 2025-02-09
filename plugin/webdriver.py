import os
import tempfile
import zipfile

from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.edge.options import Options as OptionsEdge


class Base:
    def __init__(self, host: str, port: int, user: str = None, password: str = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def apply_proxy(self):
        pass


class Chrome(Base):
    def __init__(self, host: str, port: int, user: str = None, password: str = None):
        super().__init__(host=host, port=port, user=user, password=password)

        self.manifest = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxy Auth Extension",
            "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"],
            "background": {"scripts": ["background.js"]},
            "minimum_chrome_version": "22.0.0"
        }
        """
        self.extension_path = None
        self.browser_options = None

    def proxy_config(self):
        background_js = f"""
            var config = {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "http",
                        host: "{self.host}",
                        port: parseInt({self.port})
                    }},
                    bypassList: ["localhost"]
                }}
            }};

            chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

            chrome.webRequest.onAuthRequired.addListener(
                function(details) {{
                    return {{
                        authCredentials: {{
                            username: "{self.user}",
                            password: "{self.password}"
                        }}
                    }};
                }},
                {{urls: ["<all_urls>"]}},
                ["blocking"]
            );
            """

        return background_js

    def apply_proxy(self):
        self.browser_options.add_extension(self.extension_path)

    def run(self, browser_options: OptionsChrome):
        self.extension_path = os.path.join(tempfile.gettempdir(), "selenium_proxy.zip")
        self.browser_options = browser_options

        with zipfile.ZipFile(self.extension_path, "w") as zp:  # Mount the extenson
            zp.writestr("manifest.json", self.manifest)
            zp.writestr(
                "background.js",
                self.proxy_config(),
            )

        self.apply_proxy()


class Edge(Base):
    def __init__(self, host: str, port: int, user: str = None, password: str = None):
        super().__init__(host=host, port=port, user=user, password=password)

    def apply_proxy(self):
        self.browser_options.add_argument(
            f"--proxy-server=http://{self.host}:{self.port}"
        )

        if self.user and self.password:
            self.browser_options.add_argument(
                f"--proxy-auth-basic={self.user}:{self.password}"
            )

    def run(self, browser_options: OptionsEdge):
        self.browser_options = browser_options
        self.apply_proxy()
