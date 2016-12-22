import picamera
from socketIO_client import SocketIO, LoggingNamespace
import requests
import json
from person import Person
from config import PERSON_GROUP_ID

app = 'http://helperpi-qbs19941.c9users.io'

try:
    from video_phone.face import Face
    from video_phone.person_group import PersonGroup
    from video_phone.person import Person
    from video_phone.utils import flow_one
    from .config import PERSON_GROUP_ID, IMAGE_I, IMAGE_II, IMAGE_III
except (ImportError, SystemError):
    from face import Face
    from person_group import PersonGroup
    from person import Person
    from utils import flow_one
    from config import PERSON_GROUP_ID, IMAGE_I, IMAGE_II, IMAGE_III


def on_rr_response(*args):
    f = 'temp_image.jpg'
    camera = picamera.PiCamera()
    camera.resolution = (700, 700)
    camera.capture(f)
    camera.close()
    r = requests.post('{}/upload'.format(app),
                       files={'file': (f, open(f, 'rb'), 
                       'application/vnd.ms-excel',
                       {'Expires': '0'})})
    assert r.status_code == 200
    name = flow_one(image=f)
    payload = json.dumps({'name': name})
    print(name)
    socketIO.emit('recognition response', payload)

def on_ap_request(args):
    #name = json.loads(args)['name']
    person = Person()
    person.create(group_id=PERSON_GROUP_ID, name=args)
    person.add_face(group_id=PERSON_GROUP_ID, person_id=person.pid, image='temp_image.jpg') 

if __name__ == "__main__":
    with SocketIO(app, 8080, LoggingNamespace) as socketIO:
        socketIO.on('recognition request', on_rr_response)
        socketIO.on('username update', on_ap_request)
        socketIO.wait()



