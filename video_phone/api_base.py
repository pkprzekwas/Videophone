import urllib.parse as url_parser


class ApiBase(object):
    def __init__(self):
        self.api_base = 'https://api.projectoxford.ai'
        self.api_group_operations = url_parser.urljoin(self.api_base, '/face/v1.0/persongroups/')