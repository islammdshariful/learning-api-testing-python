import json
from json import dumps

import requests

from clients.people.people_client import PeopleClient
from tests.assertions.people_assertions import *
from tests.assertions.schema_validation import assert_schema_validation
from tests.helpers.people_helpers import *
from utils.print_helpers import pretty_print

client = PeopleClient()


def test_read_all_has_person():
    response = client.read_all_persons()
    # pretty_print(response.as_dict)
    # pretty_print(response.status_code)
    # pretty_print(response.headers)
    # pretty_print(response.text)

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_people_have_person_with_first_name(response, first_name='Kent')


def test_new_person_can_be_added():
    last_name, response = client.create_person()
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)

    peoples = client.read_all_persons().as_dict
    is_new_user_created = search_created_user_in(peoples, last_name)
    assert_person_is_present(is_new_user_created)


def test_created_person_can_be_deleted():
    persons_last_name, _ = client.create_person()
    pretty_print(persons_last_name)

    peoples = client.read_all_persons().as_dict
    new_person_id = search_created_user_in(peoples, persons_last_name)['person_id']
    print(new_person_id)

    response = client.delete_person(new_person_id)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)


def test_get_all_peoples():
    response = client.read_all_persons()
    pretty_print(response.as_dict)


def test_get_specific_person():
    person_id = 6
    response = client.read_one_person_by_id(person_id)
    pretty_print(response.as_dict)


def test_delete_specific_person():
    person_id = 6
    response = client.delete_person(person_id)
    pretty_print(response.as_dict)


def test_update_specific_person():
    payload = dumps({
        "fname": "Mr.",
        "lname": "Sabbir"
    })
    person_id = 1
    client.update_person(person_id, payload=payload)

    response = client.read_one_person_by_id(person_id)
    pretty_print(response.as_dict)


def test_person_can_be_added_with_a_json_template(create_data):
    client.create_person(create_data)

    response = client.read_all_persons()
    peoples = response.as_dict

    result = search_nodes_using_json_path(peoples, json_path="$.[*].lname")

    expected_last_name = create_data['lname']
    assert_that(result).contains(expected_last_name)


def test_read_one_operation_has_expected_schema():
    person_id = 1
    response = client.read_one_person_by_id(person_id)
    person = json.loads(response.text)

    assert_schema_validation(person)


def test_read_all_operation_has_expected_schema():
    response = client.read_all_persons()
    persons = json.loads(response.text)

    assert_schema_validation(persons)
