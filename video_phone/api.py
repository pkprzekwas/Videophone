import urllib.parse as url_parser
import requests

try:
    from .config import json_headers, bin_headers, face_ids, json
    from .app_logger import logging
except (ImportError, SystemError):
    from config import json_headers, bin_headers, face_ids, json
    from app_logger import logging


class ApiBase(object):
    def __init__(self):
        self.api_base = 'https://api.projectoxford.ai'
        self.api_group_operations = url_parser.urljoin(self.api_base, '/face/v1.0/persongroups/')


class PersonGroup(ApiBase):
    def __init__(self, *, group_id):
        super(PersonGroup, self).__init__()
        self.group_id = group_id

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
        code, body = response.status_code, response.text
        if response.status_code == 200:
            logging.info("{}: {}".format(code, body))
            return code, body
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)

    def get(self) -> (int, str):
        """
        Retrieve the information of a person group,
        including its name and userData.
        """
        url = url_parser.urljoin(self.api_group_operations, '{}'.format(self.group_id))
        response = requests.get(url=url,
                                headers=json_headers)
        code, body = response.status_code, response.text
        if response.status_code == 200:
            logging.info("{}: {}".format(code, body))
            return code, body
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)

    def delete(self) -> (int, str):
        url = url_parser.urljoin(self.api_group_operations, '{}'.format(self.group_id))
        response = requests.delete(url=url,
                                   headers=json_headers)
        code, body = response.status_code, response.text
        if response.status_code == 200:
            logging.info("{}: {}".format(code, body))
            return code, body
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)

    def list(self) -> (int, str):
        """
        Retrieve the information of a person group,
        including its name and userData. This API
        returns person group information only.
        """
        url = url_parser.urljoin(self.api_group_operations, '{}/persons'.format(self.group_id))
        response = requests.get(url=url,
                                headers=json_headers)
        code, body = response.status_code, response.text
        if code == 200:
            logging.info("{}: {}".format(code, body))
            return code, body
        else:
            message = json.loads(body)['error']['message']
            raise AttributeError(message)

    def get_training_status(self) -> (int, str):
        url = url_parser.urljoin(self.api_group_operations, '{}/training'.format(self.group_id))
        response = requests.get(url=url,
                                headers=json_headers)
        code, body = response.status_code, response.text
        if response.status_code == 200:
            logging.info("{}: {}".format(code, body))
            return code, body
        else:
            message = json.loads(body)['error']['message']
            raise AttributeError(message)

    def train(self, *, person_group: str) -> None:
        url = url_parser.urljoin(self.api_group_operations, '{}/train'.format(person_group))
        response = requests.post(url=url,
                                 headers=json_headers)
        code, body = response.status_code, response.text
        if response.status_code == 202:
            logging.info("{}: {}".format(code, body))
            return code, body
        else:
            message = json.loads(body)['error']['message']
            raise AttributeError(message)


class Person(ApiBase):
    def __init__(self):
        super(Person, self).__init__()
        self.api_identify = url_parser.urljoin(self.api_base, '/face/v1.0/identify')

    def create(self, *, group_id: str, name: str) -> str:
        """
        Create a new person in a specified person group.
        A newly created person have no registered face,
        you can call Person - Add a Person Face API to add faces to the person.
        """
        url = url_parser.urljoin(self.api_group_operations, '{}/persons'.format(group_id))
        payload = {
            "name": name
        }
        response = requests.post(url=url,
                                 data=json.dumps(payload),
                                 headers=json_headers)
        if response.status_code == 200:
            logging.info("{}: {}".format(response.status_code, response.text))
            person_id = json.loads(response.text)['personId']
            return person_id
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)

    def identify(self, *, person_group: str, face_id: str) -> None:
        url = self.api_identify
        payload = {
            "personGroupId": person_group,
            "faceIds": [
                face_id
            ],
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5
        }
        response = requests.post(url=url,
                                 data=json.dumps(payload),
                                 headers=json_headers)
        if response.status_code == 200:
            logging.info("{}: {}".format(response.status_code, response.text))
            return response.status_code
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)

    def add_face(self, *, image: str, group_id: str, person_id: str, user_data: str=None) -> None:
        """
        Add a representative face to a person for identification.
        The input face is specified as an image. It returns a persistedFaceId
        representing the added face and this persistedFaceId will not expire.
        Note persistedFaceId is different from faceId which represents
        the detected face by detect_face(**kwargs).
        """
        url_end = '{}/persons/{}/persistedFaces?userData={}'.format(group_id, person_id, user_data)
        url = url_parser.urljoin(self.api_group_operations, url_end)
        binary_image = open(image, 'rb').read()
        response = requests.post(url=url,
                                 data=binary_image,
                                 headers=bin_headers
                                 )
        if response.status_code == 200:
            logging.info("{}: {}".format(response.status_code, response.text))
            return response.status_code
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)


class Face(ApiBase):
    def __init__(self):
        super(Face, self).__init__()
        self.api_detect = url_parser.urljoin(self.api_base, '/face/v1.0/detect?returnFaceId=true')

    def detect(self, *, image: str) -> str:
        """
        Detect human faces in an image and returns face id.
        """
        binary_image = open(image, 'rb').read()
        response = requests.post(url=self.api_detect,
                                 data=binary_image,
                                 headers=bin_headers)
        if response.status_code == 200:
            logging.info("{}: {}".format(response.status_code, response.text))
            face_id = json.loads(response.text)[0]['faceId']
            return face_id
        else:
            message = json.loads(response.text)['error']['message']
            raise AttributeError(message)


