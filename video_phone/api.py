import urllib.parse as url_parser
import requests

try:
    from .config import json_headers, bin_headers, face_ids, json
    from .app_logger import logging
except (ImportError, SystemError):
    from config import json_headers, bin_headers, face_ids, json
    from app_logger import logging

API_BASE = 'https://api.projectoxford.ai'
API_DETECT = url_parser.urljoin(API_BASE, '/face/v1.0/detect?returnFaceId=true')
API_IDENTIFY = url_parser.urljoin(API_BASE, '/face/v1.0/identify')
API_GROUP_OPERATIONS = url_parser.urljoin(API_BASE, '/face/v1.0/persongroups/')


def list_person_group(*, person_group: str) -> (int, str):
    """
    Retrieve the information of a person group,
    including its name and userData. This API
    returns person group information only.
    """
    url = url_parser.urljoin(API_GROUP_OPERATIONS, '{}/persons'.format(person_group))
    response = requests.get(url=url,
                            headers=json_headers)
    code, body = response.status_code, response.text
    if code == 200:
        logging.info("{}: {}".format(code, body))
        return code, body
    else:
        message = json.loads(response.text)['error']['message']
        raise AttributeError(message)


def get_person_group(*, person_group: str) -> None:
    url = url_parser.urljoin(API_GROUP_OPERATIONS, '{}'.format(person_group))
    response = requests.get(url=url,
                            headers=json_headers)
    if response.status_code == 200:
        logging.info("{}: {}".format(response.status_code, response.text))
        return response.status_code
    else:
        message = json.loads(response.text)['error']['message']
        raise AttributeError(message)


def get_training_status(*, person_group: str) -> None:
    url = url_parser.urljoin(API_GROUP_OPERATIONS, '{}/training'.format(person_group))
    response = requests.get(url=url,
                            headers=json_headers)
    if response.status_code == 200:
        logging.info("{}: {}".format(response.status_code, response.text))
        return response.status_code
    else:
        message = json.loads(response.text)['error']['message']
        raise AttributeError(message)


def train_person_group(*, person_group: str) -> None:
    url = url_parser.urljoin(API_GROUP_OPERATIONS, '{}/train'.format(person_group))
    response = requests.post(url=url,
                             headers=json_headers)
    if response.status_code == 202:
        logging.info("{}: {}".format(response.status_code, response.text))
        return response.status_code
    else:
        message = json.loads(response.text)['error']['message']
        raise AttributeError(message)


def identify_person(*, person_group: str, face_id: str) -> None:
    url = API_IDENTIFY
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


def create_person_group(*, person_list_id, name='default', user_data='') -> None:
    """
    Create a new person group with specified personGroupId,
    name and user-provided userData.
    """
    payload = {'name': name, 'userData': user_data}
    url = url_parser.urljoin(API_GROUP_OPERATIONS, person_list_id)
    response = requests.put(url=url,
                            data=json.dumps(payload),
                            headers=json_headers)
    if response.status_code == 200:
        logging.info("{}: {}".format(response.status_code, response.text))
        return response.status_code
    else:
        message = json.loads(response.text)['error']['message']
        raise AttributeError(message)


def add_face_to_person(*, image: str, group_id: str, person_id: str, user_data: str=None) -> None:
    """
    Add a representative face to a person for identification.
    The input face is specified as an image. It returns a persistedFaceId
    representing the added face and this persistedFaceId will not expire.
    Note persistedFaceId is different from faceId which represents
    the detected face by detect_face(**kwargs).
    """
    url_end = '{}/persons/{}/persistedFaces?userData={}'.format(group_id, person_id, user_data)
    url = url_parser.urljoin(API_GROUP_OPERATIONS, url_end)
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


def detect_face(*, image: str) -> str:
    """
    Detect human faces in an image and returns face id.
    """
    binary_image = open(image, 'rb').read()
    response = requests.post(url=API_DETECT,
                             data=binary_image,
                             headers=bin_headers)
    if response.status_code == 200:
        logging.info("{}: {}".format(response.status_code, response.text))
        face_id = json.loads(response.text)[0]['faceId']
        return face_id
    else:
        message = json.loads(response.text)['error']['message']
        raise AttributeError(message)


def create_person(*, group_id: str, name: str) -> str:
    """
    Create a new person in a specified person group.
    A newly created person have no registered face,
    you can call Person - Add a Person Face API to add faces to the person.
    """
    url = url_parser.urljoin(API_GROUP_OPERATIONS, '{}/persons'.format(group_id))
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
