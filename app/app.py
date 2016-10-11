import json
import urllib.parse as url_parser
import requests

from request_headers import json_headers, bin_headers

FACE_LIST_ID = 'videophone-project'
API_BASE = 'https://api.projectoxford.ai'

API_DETECT = url_parser.urljoin(API_BASE, '/detect?returnFaceId')
API_CREATE_GROUP = url_parser.urljoin(API_BASE, '/face/v1.0/persongroups/')


def create_person_group(*, person_list_id, name='default', user_data='') -> None:
    payload = {'name': name, 'userData': user_data}
    url = url_parser.urljoin(API_CREATE_GROUP, person_list_id)
    response = requests.put(url=url,
                            data=json.dumps(payload),
                            headers=json_headers)
    print("{}: {}".format(response.status_code, response.text))


def detect_face(*, image: str) -> str:
    binary_image = open(image, 'rb').read()
    response = requests.post(url=API_DETECT,
                             data=binary_image,
                             headers=bin_headers)
    print("{}: {}".format(response.status_code, response.text))

if __name__ == "__main__":
    create_person_group(person_list_id=FACE_LIST_ID,
                        name='videophone',
                        user_data='University project ETI 2016')
    pass
