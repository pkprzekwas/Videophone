import urllib.parse as url_parser
import requests

try:
    from .config import json_headers, bin_headers, face_ids, json
    from .app_logger import logging
    from .api_base import ApiBase
except (ImportError, SystemError):
    from config import json_headers, bin_headers, face_ids, json
    from app_logger import logging
    from api_base import ApiBase


class PersonGroup(ApiBase):
    def __init__(self, *, group_id):
        super(PersonGroup, self).__init__()
        self.group_id = group_id

    def __str__(self):
        return self.group_id

    def __repr__(self):
        return self.group_id

    def create(self, *, name='', user_data='') -> (int, str):
        """
        Create a new person group with specified personGroupId,
        name and user-provided userData.
        """
        payload = {'name': name, 'userData': user_data}
        url = url_parser.urljoin(self.api_group_operations, self.group_id)
        response = requests.put(url=url,
                                data=json.dumps(payload),
                                headers=json_headers)
        code, _ = self.handle_response(response)
        return code

    def get(self) -> (int, str):
        """
        Retrieve the information of a person group,
        including its name and userData.
        """
        url = url_parser.urljoin(self.api_group_operations, '{}'.format(self.group_id))
        response = requests.get(url=url,
                                headers=json_headers)
        code, _ = self.handle_response(response)
        return code

    def delete(self) -> (int, str):
        url = url_parser.urljoin(self.api_group_operations, '{}'.format(self.group_id))
        response = requests.delete(url=url,
                                   headers=json_headers)
        code, _ = self.handle_response(response)
        return code

    def list(self) -> (int, str):
        """
        Retrieve the information of a person group,
        including its name and userData. This API
        returns person group information only.
        """
        url = url_parser.urljoin(self.api_group_operations, '{}/persons'.format(self.group_id))
        response = requests.get(url=url,
                                headers=json_headers)
        code, body = self.handle_response(response)
        return code, json.loads(body)

    def get_training_status(self) -> (int, str):
        url = url_parser.urljoin(self.api_group_operations, '{}/training'.format(self.group_id))
        response = requests.get(url=url,
                                headers=json_headers)
        code, _ = self.handle_response(response)
        return code

    def train(self, *, person_group: str) -> None:
        url = url_parser.urljoin(self.api_group_operations, '{}/train'.format(person_group))
        response = requests.post(url=url,
                                 headers=json_headers)
        code, _ = self.handle_response(response)
        return code
