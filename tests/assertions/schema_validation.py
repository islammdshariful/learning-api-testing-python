from assertpy import assert_that, soft_assertions

from ..data.schema_sample import schema
from cerberus import Validator


def assert_schema_validation(persons):
    validator = Validator(schema, require_all=True)

    with soft_assertions():
        for person in persons:
            is_valid = validator.validate(person)
            assert_that(is_valid, description=validator.errors).is_true()
