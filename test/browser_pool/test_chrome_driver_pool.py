import os
from unittest import TestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from src.browser_pool import ChromeDriverPool
from src.config.webdriver_config import ChromeConfiguration
from src.exception.BrowserPoolGeneralException import BrowserPoolGeneralException
from src.exception.InvalidOrMissingConfigurationException import InvalidOrMissingConfigurationException
from src.util.webdriver_utils import get_chrome_driver_name_for_current_os

CHROME_DRIVER_DIR = os.getenv('BROWSER_POOL_WEBDRIVER_DIR', None)
CHROME_EXECUTABLE_PATH = os.path.join(CHROME_DRIVER_DIR, get_chrome_driver_name_for_current_os())
URL_GOOGLE = 'https://google.com'


def __get_headless_chrome_pool__(pool_size: int, lazy: bool):
    headless_config = ChromeConfiguration(executable_path=CHROME_EXECUTABLE_PATH, headless=True)
    return ChromeDriverPool(pool_size=pool_size, lazy_pool=lazy, chrome_config=headless_config)


def __get_headful_chrome_pool__(pool_size: int, lazy: bool):
    config = ChromeConfiguration(executable_path=CHROME_EXECUTABLE_PATH)
    return ChromeDriverPool(pool_size=pool_size, lazy_pool=lazy, chrome_config=config)


class TestChromeDriverPool(TestCase):
    def test_init_and_destroy_pool_not_raise_exceptions(self):
        pool_size = 3
        try:
            chrome_pool = __get_headless_chrome_pool__(pool_size=pool_size, lazy=False)
            chrome_pool.close_pool()
            chrome_pool = __get_headless_chrome_pool__(pool_size=pool_size, lazy=True)
            chrome_pool.close_pool()
            assert len(chrome_pool.__pool__) == 0
            assert len(chrome_pool.__preallocated_pool__) == 0
        except Exception:
            self.fail("Code raised exception unexpectedly!")

    def test_init_driver_pool_not_lazy(self):
        pool_size = 5
        chrome_pool = __get_headful_chrome_pool__(pool_size=pool_size, lazy=False)
        try:
            assert len(chrome_pool.__preallocated_pool__) == pool_size
            chrome_pool.close_pool()
        except Exception:
            chrome_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(chrome_pool.__pool__) == 0
        assert len(chrome_pool.__preallocated_pool__) == 0

    def test_headless_all_drivers_reach_correct_page(self):
        config = ChromeConfiguration(executable_path=CHROME_EXECUTABLE_PATH, headless=True)
        pool_size = 5
        chrome_pool = ChromeDriverPool(pool_size=pool_size, lazy_pool=False, chrome_config=config)
        try:
            for x in range(0, pool_size):
                session = chrome_pool.get_session()
                driver = session.driver
                driver.get(URL_GOOGLE)
                WebDriverWait(driver, timeout=10) \
                    .until(visibility_of_element_located((By.XPATH, "//img[@alt='Google']")))
                assert driver.find_element(By.XPATH, "//img[@alt='Google']") is not None
            chrome_pool.close_pool()
        except Exception:
            chrome_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(chrome_pool.__pool__) == 0
        assert len(chrome_pool.__preallocated_pool__) == 0

    def test_get_driver_returns_correct_driver(self):
        pool_size = 3
        chrome_pool = __get_headless_chrome_pool__(pool_size=pool_size, lazy=True)
        try:
            chrome_session = chrome_pool.get_session()
            assert chrome_session is not None
            assert chrome_session.session_id is not None
            assert chrome_session.driver is not None

            driver = chrome_session.driver
            driver.get(URL_GOOGLE)
            WebDriverWait(driver, timeout=10) \
                .until(visibility_of_element_located((By.XPATH, "//img[@alt='Google']")))
            assert driver.find_element(By.XPATH, "//img[@alt='Google']") is not None

            chrome_pool.close_pool()
        except Exception:
            chrome_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(chrome_pool.__pool__) == 0
        assert len(chrome_pool.__preallocated_pool__) == 0

    def test_throws_exception_when_limit_of_drivers_reached_on_lazy_pool(self):
        pool_size = 3
        chrome_pool = __get_headless_chrome_pool__(pool_size=pool_size, lazy=True)
        try:
            for x in range(0, pool_size + 1):
                chrome_pool.get_session()
        except BrowserPoolGeneralException as ex:
            chrome_pool.close_pool()
            assert ex.message == 'Reached limit of drivers in Chrome browser pool.'
        assert len(chrome_pool.__pool__) == 0
        assert len(chrome_pool.__preallocated_pool__) == 0

    def test_throws_exception_when_limit_of_drivers_reached_not_lazy_pool(self):
        pool_size = 3
        chrome_pool = __get_headless_chrome_pool__(pool_size=pool_size, lazy=False)
        try:
            for x in range(0, pool_size + 1):
                chrome_pool.get_session()
        except BrowserPoolGeneralException as ex:
            chrome_pool.close_pool()
            assert ex.message == 'Reached limit of drivers in Chrome browser pool.'
        assert len(chrome_pool.__pool__) == 0
        assert len(chrome_pool.__preallocated_pool__) == 0

    def test_add_new_driver_on_close_one_and_not_lazy_pool(self):
        pool_size = 2
        chrome_pool = __get_headful_chrome_pool__(pool_size=pool_size, lazy=False)
        try:
            assert len(chrome_pool.__pool__) == 0
            assert len(chrome_pool.__preallocated_pool__) == pool_size
            session = chrome_pool.get_session()
            assert len(chrome_pool.__pool__) == 1
            assert len(chrome_pool.__preallocated_pool__) == (pool_size - 1)
            chrome_pool.close_driver(session.session_id)
            assert len(chrome_pool.__preallocated_pool__) == pool_size
            session = next((x for x in chrome_pool.__pool__ if x.session_id == session.session_id), None)
            assert session is None
            chrome_pool.close_pool()
        except Exception:
            chrome_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(chrome_pool.__pool__) == 0
        assert len(chrome_pool.__preallocated_pool__) == 0

    def test_throws_exception_when_init_pool_with_zero_size(self):
        try:
            __get_headless_chrome_pool__(pool_size=0, lazy=True)
        except InvalidOrMissingConfigurationException as ex:
            assert ex.message == 'Pool size should be greater than 0.'

    def test_throws_exception_on_missing_executable_path(self):
        try:
            chrome_config = ChromeConfiguration(executable_path=None)
            ChromeDriverPool(pool_size=1, lazy_pool=False, chrome_config=chrome_config)
        except InvalidOrMissingConfigurationException as ex:
            assert ex.message == 'Chrome executable path should be set.'
