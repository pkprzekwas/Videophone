import pytest
import video_phone.api as api
# from video_phone.config import PERSON_GROUP_ID
PERSON_GROUP_ID = "videophone-project"
image = '../faces/mark1.jpg'
image2 = '../faces/mark2.jpg'


def test_get_list_of_persons():
    code = api.list_person_group(person_group=PERSON_GROUP_ID)
    assert code == 200
