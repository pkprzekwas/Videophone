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