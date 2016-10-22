import pytest
from uuid import uuid4
from video_phone.person_group import PersonGroup
from video_phone.person import Person


@pytest.fixture(scope='session')
def uuid():
    unique_code = uuid4()
    return str(unique_code)


@pytest.fixture(scope='session')
def uuid_person():
    unique_code = uuid4()
    return str(unique_code)


@pytest.fixture(scope='session')
def person_group(uuid):
    return PersonGroup(group_id=uuid)


@pytest.fixture(scope='session')
def created_person_group(person_group):
    person_group.create(name='test_group', user_data='test_group')
    return person_group


@pytest.fixture(scope='session')
def person():
    return Person(name='test_person')


@pytest.fixture(scope='session')
def created_person(person):
    _, _, id = person.create(name='test_person')
    return id
