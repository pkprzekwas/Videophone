import json
import urllib.parse as url_parser
try:
    from app_logger import logging
except ImportError:
    from .app_logger import logging


class ApiBase(object):
    def __init__(self):
        self.api_base = 'https://api.projectoxford.ai'
        self.api_group_operations = url_parser.urljoin(self.api_base, '/face/v1.0/persongroups/')

    @staticmethod
    def handle_response(response):
        code, body = response.status_code, response.text
        if response.status_code == 200:
            logging.info("{}: {}".format(code, body))
            return code, body
        elif response.status_code == 202:
            logging.info("code: {}".format(code))
            return code
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)
