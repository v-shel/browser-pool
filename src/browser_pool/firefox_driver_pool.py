import logging
import uuid
from typing import List

from src.config.webdriver_config import FirefoxConfiguration, FirefoxSession
from src.exception.BrowserPoolGeneralException import BrowserPoolGeneralException
from src.exception.InvalidOrMissingConfigurationException import InvalidOrMissingConfigurationException
from src.provider.webdriver_provider import provide_firefox_driver


class FirefoxDriverPool:
    def __init__(self,
                 pool_size: int = 0,
                 lazy_pool: bool = True,
                 ff_config: FirefoxConfiguration = FirefoxConfiguration()):
        self.__pool__: List[FirefoxSession] = list()
        self.__preallocated_pool__: List[FirefoxSession] = list()
        self.pool_size = pool_size
        self.lazy_pool = lazy_pool
        self.ff_config = ff_config
        self.__is_pool_ran__ = True

        self.__validate_config__()

        if not self.lazy_pool:
            self.__fill_pool__()

    def get_session(self) -> FirefoxSession:
        # When lazy pool, session instance will be created just on get_session method call and add to pool
        if self.lazy_pool:
            return self.__get_new_driver__()
        # When not lazy pool, session should be got from preallocated_pool and moved to pool
        return self.__get_preallocated_driver__()

    def close_driver(self, session_id: uuid):
        session = next((x for x in self.__pool__ if x.session_id == session_id), None)
        self.__pool__.remove(session)
        if session:
            session.driver.quit()
            if not self.lazy_pool and self.__is_pool_ran__:
                self.__preallocated_pool__.append(self.__make_new_session__())
        else:
            logging.warning('Session {} already closed or it was not started.'.format(str(session.session_id)))
        logging.info('Driver {} closed successful.'.format(str(session.session_id)))

    def __close_preallocated_drivers__(self):
        while len(self.__preallocated_pool__) > 0:
            session = self.__preallocated_pool__.pop()
            session.driver.quit()

    def close_pool(self):
        self.__is_pool_ran__ = False
        while len(self.__pool__) > 0:
            session = self.__pool__.__getitem__(0)
            self.close_driver(session.session_id)
        self.__close_preallocated_drivers__()

    def __get_new_driver__(self):
        if len(self.__pool__) == self.pool_size:
            raise BrowserPoolGeneralException('Reached limit of drivers in Firefox browser pool.')
        session = self.__make_new_session__()
        self.__pool__.append(session)
        return session

    def __get_preallocated_driver__(self):
        if len(self.__preallocated_pool__) == 0:
            raise BrowserPoolGeneralException('Reached limit of drivers in Firefox browser pool.')
        session = self.__preallocated_pool__.pop()
        self.__pool__.append(session)
        return session

    def __fill_pool__(self):
        for x in range(0, self.pool_size):
            self.__preallocated_pool__.append(self.__make_new_session__())

    def __make_new_session__(self):
        return FirefoxSession(uuid.uuid4(), provide_firefox_driver(self.ff_config))

    def __validate_config__(self):
        if not self.ff_config.executable_path:
            raise InvalidOrMissingConfigurationException('Firefox executable path should be set.')
        if self.pool_size < 1:
            raise InvalidOrMissingConfigurationException('Pool size should be greater than 0.')
