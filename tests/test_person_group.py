import pytest


def test_create_person_group(person_group, uuid):
    code = person_group.create(name=uuid, user_data=uuid)
    assert code == 200


def test_get_person_group(person_group):
    code = person_group.get()
    assert code == 200


def test_delete_person_group(person_group):
    code = person_group.delete()
    assert code == 200


def test_get_deleted_person_group(person_group):
    with pytest.raises(AttributeError) as exc_info:
        person_group.get()
