import picamera

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
    camera.capture(f)
    camera.close()
    name = flow_one(image=f)
    print(name)

if __name__ == "__main__":
    on_rr_response()


