from selenium import webdriver

from src.config.webdriver_config import ChromeConfiguration
from src.config.webdriver_config import FirefoxConfiguration


def provide_firefox_driver(ff_config: FirefoxConfiguration):
    return webdriver.Firefox(firefox_profile=ff_config.firefox_profile,
                             executable_path=ff_config.executable_path,
                             options=ff_config.options,
                             desired_capabilities=ff_config.desired_capabilities,
                             service_log_path=ff_config.service_log_path,
                             log_path=ff_config.log_path,
                             keep_alive=ff_config.keep_alive)


def provide_chrome_driver(chrome_config: ChromeConfiguration):
    return webdriver.Chrome(executable_path=chrome_config.executable_path,
                            options=chrome_config.options,
                            desired_capabilities=chrome_config.desired_capabilities,
                            service_log_path=chrome_config.service_log_path,
                            keep_alive=chrome_config.keep_alive)
