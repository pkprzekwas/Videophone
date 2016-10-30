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
    def __init__(self, *, id=None):
        super(Face, self).__init__()
        self.api_detect = url_parser.urljoin(self.api_base, '/face/v1.0/detect?returnFaceId=true')
        self.id = id

    def detect(self, *, image: str) -> str:
        """
        Detect human faces in an image and returns face id.
        """
        binary_image = open(image, 'rb').read()
        response = requests.post(url=self.api_detect,
                                 data=binary_image,
                                 headers=bin_headers)
        code, body = self.handle_response(response)
        face_id = json.loads(body)[0]['faceId']
        self.id = face_id
        return code
