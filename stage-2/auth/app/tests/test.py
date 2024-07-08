import unittest
from flask import request
import requests
from django.urls import reverse
from rest_framework import status, generics, permissions
from ..models import Organisation, User

class MyAuth(unittest.TestCase):

    def setUp(self) -> None:
        self.register_url = 'https://hng-intership.onrender.com/auth/register'
        self.login_url = 'https://hng-intership.onrender.com/auth/login'

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
        organisation = Organisation.objects.get(orgId=data['data']['user']['userId'])
        self.assertEqual(organisation.name, f"{self.payload['firstName']}'s Organisation")

    def test_login(self):
        # Register new user
        requests.post(self.register_url, data=self.payload)
        # Login as new user
        response = requests.post(self.login_url, data={"email": self.payload['email'], "password": self.payload['password']})
        response_data = response.json()
        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response_data['data']['accessToken']
        
        # Access a protected route
        userId = response_data['data']['user']['userId']
        print(f"userId: {userId}")
        getuser_url = f'https://hng-intership.onrender.com/users/{userId}'

        user_response = requests.get(getuser_url, headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})
        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_response.json().status, "success")
        print(user_response.json())


if __name__ == "__main__":
    unittest.main()