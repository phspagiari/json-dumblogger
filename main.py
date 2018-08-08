#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import dumps
from os import getenv
from socket import gethostname
from time import time, sleep

import logging
import random
import urllib2

def get_logger(application_name, log_level=1):
    logger = logging.getLogger(application_name)
    logger.setLevel(level=log_level)

    handler_stream = logging.StreamHandler()
    handler_stream.formatter = GraylogFormatter()
    logger.addHandler(handler_stream)

    # only show logs from custom formatter
    logger.propagate = False
    return logger


class GraylogFormatter(logging.Formatter):
    def __init__(self):
        self._host = gethostname()
        self._env = getenv('ENV', 'local')
        self._app = getenv('APP', 'dumbapp')
        self._product = getenv('PRODUCT', 'someproduct')
        logging.Formatter.__init__(self)

    def format(self, record):
        log = {'timestamp': time(),
               'product': self._product,
               'application': self._app,
               'environment': self._env,
               'version': '0.1',
               'host': self._host,
               'level': self.__get_log_level(record.levelno),
               'log_type': 'application',
               'full_message': record.msg}

        extra = record.args
        # if it is a dict, can be appended
        if isinstance(extra, dict):
            log.update(extra)
        return dumps(log)

    @staticmethod
    def __get_log_level(levelno):
        return {
            logging.INFO: '6',
            logging.DEBUG: '7',
            logging.ERROR: '3',
            logging.WARN: '4',
            logging.WARNING: '4',
            logging.CRITICAL: '2'
        }.get(levelno, '6')

def get_random_words():
    response = urllib2.urlopen("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain")
    txt = response.read()
    return txt.splitlines()
    
if __name__ == '__main__':
    app_name = "spagi-test" 
    logger = get_logger(application_name=app_name, log_level=6)
    words = get_random_words()


    while True:
      logger.info("Teste INFO {}".format(random.choice(words)))
      logger.debug("Teste DEBUG {}".format(random.choice(words)))
      sleep(5)


