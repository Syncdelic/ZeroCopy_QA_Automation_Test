"""Core API tests against https://reqres.in/."""
import re
import pytest
from jsonschema import validate

from . import schemas
from .conftest import API_KEY        # single source-of-truth

ISO_8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

# Header dict re-used in every call
HEADERS = {"x-api-key": API_KEY}


def test_get_users_page2(session, base_url):
    r = session.get(f"{base_url}/api/users", params={"page": 2}, headers=HEADERS)
    assert r.status_code == 200
    payload = r.json()
    validate(instance=payload, schema=schemas.list_users)
    assert payload["page"] == 2
    assert payload["data"] and all(u["email"].endswith("@reqres.in") for u in payload["data"])


@pytest.mark.parametrize("name,job", [("morpheus", "leader"), ("neo", "the one")])
def test_create_user(session, base_url, name, job):
    body = {"name": name, "job": job}
    r = session.post(f"{base_url}/api/users", json=body, headers=HEADERS)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == name and data["job"] == job
    assert data["id"].isdigit()
    assert ISO_8601.match(data["createdAt"])


def test_delete_user_2(session, base_url):
    r = session.delete(f"{base_url}/api/users/2", headers=HEADERS)
    assert r.status_code == 204
    assert r.text == ""

