from json import dumps
from uuid import uuid4

import requests
from assertpy.assertpy import assert_that

from config import BASE_URI
from utils.print_helpers import pretty_print


def test_get_all_people():
    response = requests.get(BASE_URI)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    response_tet = response.json()
    pretty_print(response_tet)


def test_has_people():
    people = get_user_url(4)
    response = requests.get(people)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    response_text = response.json()
    pretty_print(response_text)

    #For test
    # assert_that(response_text['lname']).contains('sabbir')
    # last_names = [people['lname'] for people in response_text]
    # assert_that(last_names).contains('sabbir')
    # assert_that(response.status_code).is_equal_to(200)
    # last_names = [people['lname'] for people in response_text]
    # assert_that(last_names, description='User not found').contains('sabbir')
    # pretty_print(last_names)


def test_add_people():
    unique_last_name = create_new_people()
    peoples = requests.get(BASE_URI).json()
    is_new_user_created = search_created_user_in(peoples, unique_last_name)
    assert_that(is_new_user_created, description='User not found').is_not_empty()
    pretty_print(is_new_user_created)


def test_delete_a_people():
    #For test
    # persons_last_name = create_new_people()
    # peoples = requests.get(BASE_URI).json()
    # newly_created_user = search_created_user_in(peoples, persons_last_name)[0]
    # pretty_print(newly_created_user)
    # delete_url = f'{BASE_URI}/{newly_created_user["person_id"]}'

    people = get_user_url(5)
    response = requests.delete(people)
    assert_that(response.status_code, description="User not found").is_equal_to(requests.codes.ok)

    print("People List:")
    all_pep = requests.get(BASE_URI).json()
    pretty_print(all_pep)


def test_update_people():
    person = get_user_url(4)

    payload = dumps({
        'fname': 'first name',
        'lanme': 'last name'
    })

    resource = requests.put(url=person, data=payload, headers=get_header())
    assert_that(resource.status_code, description="User not updated").is_equal_to(requests.codes.ok)
    usr = requests.get(person).json()
    pretty_print(usr)


def get_user_url(id):
    url = f'{BASE_URI}/{id}'
    return url


def get_header():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return headers


def create_new_people():
    # Ensure a user with a unique last name is created everytime the test runs
    # Note: json.dumps() is used to convert python dict to json string
    unique_last_name = f'User {str(uuid4())}'
    payload = dumps({
        'fname': 'New',
        'lname': unique_last_name
    })

    # Setting default headers to show that the client accepts json
    # And will send json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # We use requests.post method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=get_header())
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name


def search_created_user_in(peoples, last_name):
    return [person for person in peoples if person['lname'] == last_name]