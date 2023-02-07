import os

from src.exception.UnsupportedOperationSystemException import UnsupportedOperationSystemException

GECKODRIVER = 'geckodriver'
CHROMEDRIVER = 'chromedriver'


def get_chrome_driver_name_for_current_os():
    system = os.name
    if system == 'nt':
        return CHROMEDRIVER + '.exe'
    elif system == 'posix':
        return CHROMEDRIVER
    raise UnsupportedOperationSystemException()


def get_firefox_driver_name_for_current_os():
    system = os.name
    if system == 'nt':
        return GECKODRIVER + '.exe'
    elif system == 'posix':
        return GECKODRIVER
    raise UnsupportedOperationSystemException()
