import pytest
from uuid import uuid4
from video_phone.api import PersonGroup

image = '../faces/mark1.jpg'
image2 = '../faces/mark2.jpg'


@pytest.fixture(scope='session')
def uuid():
    unique_code = uuid4()
    return str(unique_code)


@pytest.fixture(scope='session')
def person_group(uuid):
    return PersonGroup(group_id=uuid)


def test_create_person_group(person_group, uuid):
    code, _ = person_group.create(name=uuid, user_data=uuid)
    assert code == 200


def test_get_person_group(person_group):
    code, _ = person_group.get()
    assert code == 200


def test_delete_person_group(person_group):
    code, _ = person_group.delete()
    assert code == 200


def test_get_deleted_person_group(person_group):
    with pytest.raises(AttributeError) as exc_info:
        code, _ = person_group.get()