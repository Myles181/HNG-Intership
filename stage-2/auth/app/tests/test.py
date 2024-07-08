import unittest
from flask import request
import requests
from django.urls import reverse
from rest_framework import status, generics, permissions
from ..models import Organisation, User

class MyAuth(unittest.TestCase):

    def setUp(self) -> None:
        self.register_url = 'http://127.0.0.1:8000/auth/register'
        self.login_url = 'http://127.0.0.1:8000/auth/login'

        self.payload = {
            "firstName": "Micheal",
            "lastName": "John",
            "email": "micheal@gmail.com",
            "password": "john12345",
            "phone": "0802348568350"
        }
# python -m unittest -v auth.spec.Testing
    def tearDown(self) -> None:
        print("In tearDown")
        try:
            user = User.objects.get(email=self.payload['email'])
            user.organisations.all().delete()
            user.delete()
        except User.DoesNotExist:
            pass

    def test_register(self):
        response = requests.post(self.register_url, data=self.payload)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organisation = Organisation.objects.get(orgId=data['data']['userId'])
        print(organisation)
        # self.assertAlmostEqual()


if __name__ == "__main__":
    unittest.main()