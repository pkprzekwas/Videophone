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


def flow_one(group_id=PERSON_GROUP_ID, image=IMAGE_II):
    person_group = PersonGroup(group_id=group_id)
    face = Face()
    person = Person()
    face.detect(image=image)
    person.identify(person_group=person_group.group_id, face_id=face.id)
    if person.has_id:
        person_group = PersonGroup(group_id=group_id)
        _, body = person_group.list()
        for each in body:
            if person.id == each['personId']:
                print('{} : {}'.format(each['name'], each['personId']))
    else:
        print("What's your name?: ")
        name = input('--> ')
        person.create(group_id=group_id, name=name)
        person.add_face(image=image)
        print('{} : {}'.format(person.name, person.id))


def clear_group(group_id):
    person_group = PersonGroup(group_id=group_id)
    _, body = person_group.list()
    body = json.loads(body)
    for each in body:
        print('{} : {}'.format(each['name'], each['personId']))
        temp = Person(id=each['personId'])
        temp.delete(group_id=PERSON_GROUP_ID)
    pass


if __name__ == "__main__":
    flow_one()
