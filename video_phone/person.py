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


class Person(ApiBase):
    def __init__(self, *, name: str=None, pid: str=None):
        super(Person, self).__init__()
        self.api_identify = url_parser.urljoin(self.api_base, '/face/v1.0/identify')
        self.name = name
        self.pid = pid
        self.has_pid = True if self.pid is not None else False

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
        code, body = self.handle_response(response)
        person_id = json.loads(body)['personId']
        self.pid = person_id
        self.has_pid = True
        self.name = name
        return code

    def delete(self, group_id: str):
        url = url_parser.urljoin(self.api_group_operations, '{}/persons/{}'.format(group_id, self.pid))
        response = requests.delete(url=url,
                                   headers=json_headers)
        code, _ = self.handle_response(response)
        return code

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
        code, body = self.handle_response(response)
        candidates = json.loads(body)[0]['candidates']
        if candidates:
            self.pid = candidates[0]['personId']
            self.has_pid = True
        return code

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
        code, _ = self.handle_response(response)
        return code
