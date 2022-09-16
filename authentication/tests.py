from authentication.models import User
# from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient, APITestCase


# Create your tests here.
class AuthenticationTestCase(APITestCase):
    def setup(self):
        self.user = User.objects.create_user(email="jishnu@gmail.com", password= "12345678")

    def test_login_session(self):
        client = APIClient()
        client.login(username='jishnun789@gmail.com', password='12345')


    def test_api_jwt(self):
        
        # signup user
        u = User.objects.create_user(email='user@foo.com', password='password12-')
        u.is_active = False
        u.save()

        # trying to login before crated user is made active, similar to login before signup
        resp = self.client.post('/user/login/', {'email':'user@foo.com', 'password':'password12-'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # print(resp.data)

        u.is_active = True
        u.save()

        #login after user is added to database as active user
        resp = self.client.post('/user/login/', {'email':'user@foo.com', 'password':'password12-'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # print(resp.data)
        self.assertTrue('access' in resp.data)
        token = resp.data['access']

        client = APIClient()

        # trying to login with invalid jwt token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        resp = client.get('/user/login_test/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # trying to login with actual token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = client.get('/user/login_test/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)