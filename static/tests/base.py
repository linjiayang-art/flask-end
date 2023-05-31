import unittest

from flask import url_for

from static import create_app
from static.extensions import db
from static.models import User
from static.forms import LoginFrom
from static.factory import to_dict
class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app=create_app('testing')
        self.context=app.test_request_context()
        self.context.push()
        self.client=app.test_client()
        self.runner=app.test_cli_runner()

        db.create_all()
        user=User(userno='666',username='linyang')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()
    
    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self,username=None,password=None):
        if username is None and password is None:
            username='linyang'
            password='123'

        return self.client.post(url_for('auth.login'),data=dict(
            username=username,
            password=password
        ),follow_redirects=True)
    
class BaseAPITestCase(unittest.TestCase):

    def setUp(self):
        app=create_app('testing')
        self.context=app.test_request_context()
        self.context.push()
        self.client=app.test_client()
        self.runner=app.test_cli_runner()
        db.create_all()
        user=User(userno='123456',username='linyang')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
    
    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def get_oauth_token(self):
        response=self.client.post(url_for('api_v1.token'),data=dict(
            userno='123456',
            password='123456'
        ))
        data=response.get_json()
        #return data['access_token']
        return data['data']['access_token']
    def set_auth_headers(self, token):
        return {
            #'Authorization': token,
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_token(self):
        response = self.client.post(url_for('api_v1.token'), data=dict(
            userno='123456',
            password='123456'
        ))
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data['data'])    
        self.assertIn('statusText', data['data']) 
        self.assertIn('csrf_token', data['data']) 
        self.assertIn('access_token', data['data'])   
        self.assertIn('expires',data['data'])
        self.assertIn('username',data['data'])
        self.assertIn('userno',data['data'])
        self.assertEqual(True,data['success'])

    def test_erro_get_token(self):
        response = self.client.post(url_for('api_v1.token'), data=dict(
            userno='12345678',
            password='123456'
        ))
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('code', data)
        self.assertIn('msg', data)
        self.assertIn(data['code'],'B0001') 

    def test_noform_get_token(self):
        response = self.client.post(url_for('api_v1.token'))
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('code', data)
        self.assertIn('msg', data)
        self.assertIn(data['code'],'201') 
        self.assertIn('表单',data['msg']) 

    def test_logout(self):
        response=self.client.delete(url_for('api_v1.logout'))
        data=response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertIn('code', data)
        self.assertIn(data['code'],'A230') 