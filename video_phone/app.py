import picamera
import requests
from socketIO_client import SocketIO, LoggingNamespace

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
    f = 'image.jpg'
    camera = picamera.PiCamera()
    camera.capture(f)
    camera.close()
    r = requests.post('{}/upload'.format(app),
                      files={'file': (f, open(f, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})})
    assert r.status_code == 200
    name = flow_one(image=f)
    r = requests.post('{}/upload'.format(app),
                      headers='application/json', body=name)
    assert r.status_code == 200
    socketIO.emit('recognition response')

if __name__ == "__main__":
    with SocketIO(app, 8080, LoggingNamespace) as socketIO:
        socketIO.on('recognition request', on_rr_response)
        socketIO.wait()


