import uuid
from typing import Dict, Union

from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.webdriver.chrome import webdriver as chrome_driver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox import webdriver as firefox_driver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class FirefoxSession:
    def __init__(self, session_id: uuid = None, driver: firefox_driver = None):
        self.session_id: uuid = session_id
        self.driver: firefox_driver = driver


def add_capability(capabilities: Dict[str, Union[str, bool]], name: str, value: Union[str, bool]):
    capabilities[name] = value


def set_proxy(capabilities: Dict[str, Union[str, bool]], proxy: str):
    add_capability(capabilities, "proxy", Union["proxyType", "manual"])
    add_capability(capabilities, "proxy", Union["httpProxy", proxy])
    add_capability(capabilities, "proxy", Union["ftpProxy", proxy])
    add_capability(capabilities, "proxy", Union["sslProxy", proxy])


class FirefoxConfiguration:
    def __init__(self,
                 firefox_profile: FirefoxProfile = None,
                 proxy: str = None,
                 executable_path: str = None,
                 options: FirefoxOptions = FirefoxOptions(),
                 desired_capabilities: Dict[str, Union[str, bool]] = DesiredCapabilities.FIREFOX,
                 page_load_strategy: str = None,
                 log_path: str = None,
                 service_log_path: str = None,
                 keep_alive: bool = True,
                 headless: bool = False):
        self.firefox_profile = firefox_profile
        self.proxy = proxy
        self.executable_path = executable_path
        self.options = options
        self.desired_capabilities = desired_capabilities
        self.log_path = log_path
        self.service_log_path = service_log_path
        self.keep_alive = keep_alive

        self.options.headless = headless
        if page_load_strategy:
            self.options.page_load_strategy = page_load_strategy

    def set_profile(self, firefox_profile: FirefoxProfile):
        self.firefox_profile = firefox_profile

    def with_proxy(self, proxy: str):
        set_proxy(self.desired_capabilities, proxy)

    def set_executable_path(self, executable_path: str):
        self.executable_path = executable_path

    def set_options(self, options: FirefoxOptions):
        self.options = options

    def add_option(self, argument):
        self.options.add_argument(argument)

    def set_capabilities(self, desired_capabilities: Dict[str, Union[str, bool]]):
        self.desired_capabilities = desired_capabilities

    def add_capability(self, name: str, value: Union[str, bool]):
        add_capability(self.desired_capabilities, name, value)

    def set_default_capabilities(self):
        self.desired_capabilities = FirefoxOptions.default_capabilities

    def set_log_path(self, log_path: str):
        self.log_path = log_path

    def set_service_log_path(self, service_log_path: str):
        self.service_log_path = service_log_path

    def set_keep_alive(self, keep_alive: bool):
        self.keep_alive = keep_alive


class ChromeSession:
    def __init__(self, session_id: uuid = None, driver: chrome_driver = None):
        self.session_id: uuid = session_id
        self.driver: chrome_driver = driver


class ChromeConfiguration:
    def __init__(self,
                 proxy: str = None,
                 executable_path: str = None,
                 options: ChromeOptions = ChromeOptions(),
                 desired_capabilities: Dict[str, Union[str, bool]] = DesiredCapabilities.CHROME,
                 page_load_strategy: str = None,
                 log_path: str = None,
                 service_log_path: str = None,
                 keep_alive: bool = True,
                 headless: bool = False):
        self.proxy = proxy
        self.executable_path = executable_path
        self.options = options
        self.desired_capabilities = desired_capabilities
        self.log_path = log_path
        self.service_log_path = service_log_path
        self.keep_alive = keep_alive

        self.options.headless = headless
        if page_load_strategy:
            self.options.page_load_strategy = page_load_strategy

    def set_proxy(self, proxy: str):
        set_proxy(self.desired_capabilities, proxy)

    def set_executable_path(self, executable_path: str):
        self.executable_path = executable_path

    def set_options(self, options: ChromeOptions):
        self.options = options

    def add_option(self, argument):
        self.options.add_argument(argument)

    def set_capabilities(self, desired_capabilities: Dict[str, Union[str, bool]]):
        self.desired_capabilities = desired_capabilities

    def add_capability(self, name: str, value: Union[str, bool]):
        add_capability(self.desired_capabilities, name, value)

    def set_default_capabilities(self):
        self.desired_capabilities = ChromeOptions.default_capabilities

    def set_service_log_path(self, service_log_path: str):
        self.service_log_path = service_log_path

    def set_keep_alive(self, keep_alive: bool):
        self.keep_alive = keep_alive
