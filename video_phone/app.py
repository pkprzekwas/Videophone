try:
    import app.api as api
    from .config import PERSON_GROUP_ID
except (ImportError, SystemError):
    import api
    from config import PERSON_GROUP_ID

image = '../faces/mark1.jpg'
image2 = '../faces/mark2.jpg'


def add_new_person_to_group(*, image, name, group):
    person_id = api.create_person(group_id=PERSON_GROUP_ID, name='Mark1')
    api.add_face_to_person(image=image, group_id=PERSON_GROUP_ID,
                           person_id=person_id, user_data='Mark\'s face')


def train(*, person_group=PERSON_GROUP_ID):
    api.train_person_group(person_group=person_group)
    api.get_person_group(person_group=person_group)
    api.get_training_status(person_group=person_group)


def identify(*, image, person_group=PERSON_GROUP_ID):
    face_id = api.detect_face(image=image)
    print(face_id)
    api.identify_person(person_group=person_group, face_id=face_id)


if __name__ == "__main__":
    # our group has been already created
    if False:
        api.create_person_group(person_list_id=PERSON_GROUP_ID,
                                name='videophone',
                                user_data='University project ETI 2016')
        face_id = api.detect_face(image=image)
        person_id = api.create_person(group_id=PERSON_GROUP_ID, name='Mark1')
        api.add_face_to_person(image=image, group_id=PERSON_GROUP_ID,
                               person_id=person_id, user_data='Mark\'s face')
        face_id = api.detect_face(image=image)
        print(face_id)
        api.identify_person(person_group=PERSON_GROUP_ID, face_id=face_id)
    add_new_person_to_group(image=image, name='Obama1', group=PERSON_GROUP_ID)
    train(person_group=PERSON_GROUP_ID)
    identify(image=image2)