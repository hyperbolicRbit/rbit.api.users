# project/tests/test_user_model.py


import json

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('justatest', 'test@test.com', 'testpw')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)
        self.assertTrue(user.admin == False)

    def test_add_user_duplicate_username(self):
        add_user('justatest', 'test@test.com', 'testpw')
        duplicate_user = User(
                username='justatest',
                password='test',
                email='test@test2.com',
                )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('justatest', 'test@test.com', 'testpw')
        duplicate_user = User(
                username='justatest2',
                password='test',
                email='test@test.com',
                )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'test@test.com', 'test')
        user_two = add_user('justatest2', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_aut_token(self):
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token), user.id)

    def test_add_user_not_admin(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            # user login
            resp_login = self.client.post(
                    '/auth/login',
                    data=json.dumps(dict(
                        email='test@test.com',
                        password='test'
                        )),
                    content_type='application/json'
                    )
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='michael',
                        email='michael@realpython.com',
                        password='test'
                        )),
                    content_type='application/json',
                    headers=dict(
                        Authorization='Bearer ' + json.loads(
                            resp_login.data.decode()
                            )['auth_token']
                        )
                    )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                    data['message'] == 'You do not have permission to do that.')
            self.assertEqual(response.status_code, 401)
