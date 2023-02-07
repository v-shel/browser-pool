import os
from unittest import TestCase

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from src.browser_pool.firefox_driver_pool import FirefoxDriverPool
from src.config.webdriver_config import FirefoxConfiguration
from src.exception.BrowserPoolGeneralException import BrowserPoolGeneralException
from src.exception.InvalidOrMissingConfigurationException import InvalidOrMissingConfigurationException
from src.util.webdriver_utils import get_firefox_driver_name_for_current_os

FIREFOX_DRIVER_DIR = os.getenv('BROWSER_POOL_WEBDRIVER_DIR', None)
FIREFOX_EXECUTABLE_PATH = os.path.join(FIREFOX_DRIVER_DIR, get_firefox_driver_name_for_current_os())
URL_GOOGLE = 'https://google.com'


def __get_headless_ff_pool__(pool_size: int, lazy: bool):
    headless_config = FirefoxConfiguration(executable_path=FIREFOX_EXECUTABLE_PATH, headless=True)
    return FirefoxDriverPool(pool_size=pool_size, lazy_pool=lazy, ff_config=headless_config)


def __get_headful_ff_pool__(pool_size: int, lazy: bool):
    config = FirefoxConfiguration(executable_path=FIREFOX_EXECUTABLE_PATH)
    return FirefoxDriverPool(pool_size=pool_size, lazy_pool=lazy, ff_config=config)


class TestFirefoxDriverPool(TestCase):
    def test_init_and_destroy_pool_not_raise_exceptions(self):
        pool_size = 3
        try:
            ff_pool = __get_headless_ff_pool__(pool_size=pool_size, lazy=False)
            ff_pool.close_pool()
            ff_pool = __get_headless_ff_pool__(pool_size=pool_size, lazy=True)
            ff_pool.close_pool()
            assert len(ff_pool.__pool__) == 0
            assert len(ff_pool.__preallocated_pool__) == 0
        except Exception:
            self.fail("Code raised exception unexpectedly!")

    def test_init_driver_pool_not_lazy(self):
        pool_size = 5
        ff_pool = __get_headful_ff_pool__(pool_size=pool_size, lazy=False)
        try:
            assert len(ff_pool.__preallocated_pool__) == pool_size
            ff_pool.close_pool()
        except Exception:
            ff_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(ff_pool.__pool__) == 0
        assert len(ff_pool.__preallocated_pool__) == 0

    def test_headless_all_drivers_reach_correct_page(self):
        default_ff_headless_config = FirefoxConfiguration(executable_path=FIREFOX_EXECUTABLE_PATH, headless=True)
        pool_size = 5
        ff_pool = FirefoxDriverPool(pool_size=pool_size, lazy_pool=False, ff_config=default_ff_headless_config)
        try:
            for x in range(0, pool_size):
                session = ff_pool.get_session()
                driver = session.driver
                driver.get(URL_GOOGLE)
                WebDriverWait(driver, timeout=10) \
                    .until(visibility_of_element_located((By.XPATH, "//img[@alt='Google']")))
                assert driver.find_element(By.XPATH, "//img[@alt='Google']") is not None
            ff_pool.close_pool()
        except Exception:
            ff_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(ff_pool.__pool__) == 0
        assert len(ff_pool.__preallocated_pool__) == 0

    def test_get_driver_returns_correct_driver(self):
        pool_size = 3
        ff_pool = __get_headless_ff_pool__(pool_size=pool_size, lazy=True)
        try:
            ff_session = ff_pool.get_session()
            assert ff_session is not None
            assert ff_session.session_id is not None
            assert ff_session.driver is not None

            driver = ff_session.driver
            driver.get(URL_GOOGLE)
            WebDriverWait(driver, timeout=10) \
                .until(visibility_of_element_located((By.XPATH, "//img[@alt='Google']")))
            assert driver.find_element(By.XPATH, "//img[@alt='Google']") is not None

            ff_pool.close_pool()
        except Exception:
            ff_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(ff_pool.__pool__) == 0
        assert len(ff_pool.__preallocated_pool__) == 0

    def test_throws_exception_when_limit_of_drivers_reached_on_lazy_pool(self):
        pool_size = 3
        ff_pool = __get_headless_ff_pool__(pool_size=pool_size, lazy=True)
        try:
            for x in range(0, pool_size + 1):
                ff_pool.get_session()
        except BrowserPoolGeneralException as ex:
            ff_pool.close_pool()
            assert ex.message == 'Reached limit of drivers in Firefox browser pool.'
        assert len(ff_pool.__pool__) == 0
        assert len(ff_pool.__preallocated_pool__) == 0

    def test_throws_exception_when_limit_of_drivers_reached_not_lazy_pool(self):
        pool_size = 3
        ff_pool = __get_headless_ff_pool__(pool_size=pool_size, lazy=False)
        try:
            for x in range(0, pool_size + 1):
                ff_pool.get_session()
        except BrowserPoolGeneralException as ex:
            ff_pool.close_pool()
            assert ex.message == 'Reached limit of drivers in Firefox browser pool.'
        assert len(ff_pool.__pool__) == 0
        assert len(ff_pool.__preallocated_pool__) == 0

    def test_add_new_driver_on_close_one_and_not_lazy_pool(self):
        pool_size = 2
        ff_pool = __get_headful_ff_pool__(pool_size=pool_size, lazy=False)
        try:
            assert len(ff_pool.__pool__) == 0
            assert len(ff_pool.__preallocated_pool__) == pool_size
            session = ff_pool.get_session()
            assert len(ff_pool.__pool__) == 1
            assert len(ff_pool.__preallocated_pool__) == (pool_size - 1)
            ff_pool.close_driver(session.session_id)
            assert len(ff_pool.__preallocated_pool__) == pool_size
            session = next((x for x in ff_pool.__pool__ if x.session_id == session.session_id), None)
            assert session is None
            ff_pool.close_pool()
        except Exception:
            ff_pool.close_pool()
            self.fail("Code raised exception unexpectedly!")
        assert len(ff_pool.__pool__) == 0
        assert len(ff_pool.__preallocated_pool__) == 0

    def test_throws_exception_when_init_pool_with_zero_size(self):
        try:
            __get_headless_ff_pool__(pool_size=0, lazy=True)
        except InvalidOrMissingConfigurationException as ex:
            assert ex.message == 'Pool size should be greater than 0.'

    def test_throws_exception_on_missing_executable_path(self):
        try:
            ff_config = FirefoxConfiguration(executable_path=None)
            FirefoxDriverPool(pool_size=1, lazy_pool=False, ff_config=ff_config)
        except InvalidOrMissingConfigurationException as ex:
            assert ex.message == 'Firefox executable path should be set.'
