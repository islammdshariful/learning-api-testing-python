import random
from json import dumps, loads
from uuid import uuid4

import pytest
import requests
from assertpy.assertpy import assert_that
from jsonpath_ng import parse

from config import BASE_URI
from utils.file_reader import read_file
from utils.print_helpers import pretty_print


# @pytest.fixture
# def create_data():
#     payload = read_file('create_person.json')
#
#     random_no = random.randint(0, 1000)
#     last_name = f'Olabini{random_no}'
#
#     payload['lname'] = last_name
#     yield payload


def test_person_can_be_added_with_a_json_template(create_data):
    create_person_with_unique_last_name(create_data)

    response = requests.get(BASE_URI)
    peoples = loads(response.text)  # 'jason.loads = read json data from text and covert to python dictionary'
    pretty_print(peoples)

    # Get all last names for any object in the root array
    # Here $ = root, [*] represents any element in the array
    jsonpath_expr = parse("$.[*].lname")
    result = [match.value for match in jsonpath_expr.find(peoples)]
    print(result)
    expected_last_name = create_data['lname']
    assert_that(result).contains(expected_last_name)


def create_person_with_unique_last_name(body=None):
    if body is None:
        unique_last_name = f'User {str(uuid4())}'
        payload = dumps({
            'fname': 'New',
            'lname': unique_last_name
        })
    else:
        unique_last_name = body['lname']
        payload = dumps(body)

    # Setting default headers to show that the client accepts json
    # And will send json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # We use requests.post method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name


def search_created_user_in(peoples, last_name):
    return [person for person in peoples if person['lname'] == last_name]
