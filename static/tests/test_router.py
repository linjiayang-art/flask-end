from static.tests.base import BaseAPITestCase
from flask import url_for
from static.models.usermodel import User
from static.extensions import db


class RouetrTestCase(BaseAPITestCase):

    def test_get_router(self):
        token = self.get_oauth_token()
        response = self.client.get(url_for('api_v1.routes'),
                                   headers=self.set_auth_headers(token))
        data = response.get_json()
        self.assertIn('code', data)
        self.assertIn('data', data)
