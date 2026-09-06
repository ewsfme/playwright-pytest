"""Generates randomized, unique test data using Faker.

Using randomly generated values (rather than hardcoded ones) keeps the
suite runnable multiple times against the same live site without
"email already exists" collisions, and satisfies the requirement to
use randomized input data.
"""
import random
import string

from faker import Faker

fake = Faker()


def random_email() -> str:
    unique_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"qa.{unique_suffix}@mailinator.com"


def random_name() -> str:
    return fake.name()


def random_password() -> str:
    return fake.password(length=12)


def random_account_data() -> dict:
    return {
        "password": random_password(),
        "dob_day": str(random.randint(1, 28)),
        "dob_month": str(random.randint(1, 12)),
        "dob_year": str(random.randint(1970, 2002)),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": fake.secondary_address(),
        "country": random.choice(["United States", "Canada", "Australia", "New Zealand", "Singapore"]),
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.postcode(),
        "mobile_number": fake.numerify("##########"),
    }


def random_contact_message() -> dict:
    return {
        "name": fake.name(),
        "email": random_email(),
        "subject": fake.sentence(nb_words=4),
        "message": fake.paragraph(nb_sentences=3),
    }
