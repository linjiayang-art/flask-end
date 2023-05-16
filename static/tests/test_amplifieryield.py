from static.tests.base import BaseAPITestCase
from flask import url_for
from static.extensions import db

class TsetAmplifier(BaseAPITestCase):
    def test_get_lot(self):
        token = self.get_oauth_token()
        response = self.client.get(url_for('api_v1.menus'), headers=self.set_auth_headers(token))
        data = response.get_json()
        sql="select *From limit_production  WHERE chip_type='PowerGain' and chip='SIA071SP3' "
        result_proxy = db.session.execute(
            sql, bind=db.get_engine(bind_key='sicore'))
        print(result_proxy)