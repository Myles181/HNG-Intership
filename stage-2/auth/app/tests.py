import unittest
from flask import request
import requests
from django.urls import reverse
from rest_framework import status, generics, permissions
from .models import Organisation, User

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

    def tearDown(self) -> None:
        print("In tearDown")
        try:
            user = User.objects.get(email=self.payload['email'])
            organisation = Organisation.objects.get(user=user)
            organisation.delete()
            user.delete()
        except User.DoesNotExist:
            pass

    def test_register_success(self):
        response = requests.post(self.register_url, data=self.payload)
        print(response.json())  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_fail(self):
        data = self.payload.copy()
        data.pop('firstName')
        response = requests.post(self.register_url, data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.json())
        self.assertEqual(response.json()['errors'][0]['field'], 'phone')

    # def test_login_success(self):
    #     data = {'email': self.payload['email'], 'password': self.payload['password']}
    #     response = requests.post(self.login_url, data=data)
    #     print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_login_fail(self):
    #     data = {'email': self.payload['email'], 'password': self.payload['password']}
    #     response = requests.post(self.login_url, data=data)
    #     print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)



if __name__ == "__main__":
    unittest.main()