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


def flow_one(group_id=PERSON_GROUP_ID, image=IMAGE_III):
    person_group = PersonGroup(group_id=group_id)
    person_group.train(group_id=group_id)
    face = Face()
    person = Person()
    code = face.detect(image=image)
    if code != 200:
        return 'No face was detected'
    person.identify(person_group=person_group.group_id, face_id=face.id)
    if person.has_pid:
        _, body = person_group.list()
        for each in body:
            if person.pid == each['personId']:
                print('{} : {}'.format(each['name'], each['personId']))
                return each['name']
    else:
        print("What's your name?: ")
        name = input('--> ')
        person.create(group_id=group_id, name=name)
        person.add_face(group_id=group_id, person_id=person.pid, image=image)
        print('{} : {}'.format(person.name, person.pid))
        return person.name


def create_group(name, user_data):
    p = PersonGroup(group_id=PERSON_GROUP_ID)
    p.create(name=name, user_data=user_data)


def clear_group(group_id):
    person_group = PersonGroup(group_id=group_id)
    _, body = person_group.list()
    body = json.loads(body)
    for each in body:
        print('{} : {}'.format(each['name'], each['personId']))
        temp = Person(pid=each['personId'])
        temp.delete(group_id=PERSON_GROUP_ID)
