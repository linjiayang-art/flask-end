from static.tests.base import BaseAPITestCase
from flask import url_for

class UserInfoTestCase(BaseAPITestCase):
    def test_get_userinfo(self):
        token = self.get_oauth_token()
        response = self.client.get(url_for('api_v1.userinfoapi'),
                                   headers=self.set_auth_headers(token))
        data=response.get_json()
        self.assertIn('code', data)
        self.assertIn('data', data)