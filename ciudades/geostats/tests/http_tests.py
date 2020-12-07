import requests
import pytest
from django.test import Client

from ciudades.geostats.models import *
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        if User.objects.filter(pk=110).exists():
            return
        user, new = User.objects.get_or_create(
            email="test@tesmail.com",
            first_name="test",
            id=110,
            password="test0Test",
            username="test45678"
        )


@pytest.mark.django_db
class TestNavigation:
    client = None
    site = "http://localhost:8000"

    def test_login(self):
        c = Client()
        logged_in = c.login(username="test45678", password="test0Test")
        assert logged_in is True and int(c.session['_auth_user_id']) is 110
        self.client = c
        reqs = [
            {"type": "POST", "url": "/do_login/", "params": {"uname":"test", "pswd":"test"}},
            {"type": "GET", "url": "/", "params": {}}, # Check we are getting logged in results
            {"type": "GET", "url": "/logout", "params": {}}
            # Include here any other requests to be tested
        ]
        for req in reqs :
            resp = c.request(method=req.get("type"), url= "{self.site}{req.get('url')}", json=req.get("params"))
            assert resp.status_code >= 200 and resp.status_code < 300

