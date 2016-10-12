import api
from config import PERSON_GROUP_ID

image = '../faces/mark1.jpg'

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



