import json

try:
    from video_phone.face import Face
    from video_phone.person_group import PersonGroup
    from video_phone.person import Person
    from .config import PERSON_GROUP_ID, IMAGE_I, IMAGE_II, IMAGE_III
except (ImportError, SystemError):
    from face import Face
    from person_group import PersonGroup
    from person import Person
    from config import PERSON_GROUP_ID, IMAGE_I, IMAGE_II, IMAGE_III


def flow_one():
    person_group = PersonGroup(group_id=PERSON_GROUP_ID)
    face = Face()
    person = Person()
    face.detect(image=IMAGE_II)
    person.identify(person_group=person_group.group_id, face_id=face.id)
    print(person.id)
    _, body = person_group.list()
    body = json.loads(body)
    for each in body:
        print('{} : {}'.format(each['name'], each['personId']))
        # temp = Person(id=each['personId'])
        # temp.delete(group_id=PERSON_GROUP_ID)
    pass


if __name__ == "__main__":
    flow_one()