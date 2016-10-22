import pytest


def test_create_person(person, created_person_group):
    code, _, id = person.create(group_id=created_person_group, name='test_person')
    assert code == 200


def test_list_persons(person_group):
    code, body = person_group.list()
    assert code == 200


def test_delete_person(person, created_person_group, person_group):
    try:
        code, _ = person.delete(group_id=created_person_group)
        assert code == 200
    finally:
        person_group.delete()
