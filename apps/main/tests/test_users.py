# Python


# Django
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
# Rest Framework

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

TEST_USER1 = 'test1@example.com'
TEST_USER2 = 'test2@example.com'
TEST_USER3 = 'test3@example.com'
TEST_USER4 = 'test4@example.com'
CURRENT_PASSWORD = 'current_password_123'
NEW_PASSWORD = 'new_password_123'
WRONG_PASSWORD = 'wrong_password_123'
WRONG_TOKEN = '11111111-2222-3333-4444-555555555555'


def authentication(username, password):
    url = reverse('main:auth')
    data = {'username': username, 'password': password}

    client = APIClient()
    return client.post(url, data, format='json')


def get_token(username=TEST_USER1, password=CURRENT_PASSWORD):
    # Authentication
    response = authentication(username, password)
    return response.data['token']


def get_token_simple_user(username=TEST_USER2, password=CURRENT_PASSWORD):
    # Authentication
    response = authentication(username, password)
    return response.data['token']


class UserAuthTest(APITestCase):
    fixtures = ['users.yaml', ]

    def test_user_auth_success(self):
        # Authentication
        response = authentication(TEST_USER1, CURRENT_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Authentication
        response = authentication(TEST_USER2, CURRENT_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_auth_fail(self):
        url = reverse('main:auth')
        data = {'username': TEST_USER1, 'password': WRONG_TOKEN}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_auth_invalid_params(self):
        # self made auth test
        url = reverse('main:auth')

        response = self.client.post(url, {})
        self.assertEqual(response.data['password'][0], _('This field is required.'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # django rest_framework auth test
        url = reverse('login')

        response = self.client.post(url, {})
        self.assertEqual(response.data['password'][0], _('This field is required.'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserUnAuthTest(APITestCase):
    fixtures = ['users.yaml', ]

    def test_user_unauth_success(self):
        # Authentication
        response = authentication(TEST_USER1, CURRENT_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserCrudTest(APITestCase):
    fixtures = [
        'users.yaml',
    ]

    list_url = 'main:user-list'
    detail_url = 'main:user-detail'
    user_info_url = 'main:user-info'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_detail(self):
        url = reverse(self.user_info_url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test1@example.com')

    def test_user_logout(self):
        # Unauthorized
        url = reverse('main:user-logout')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        url = reverse(self.detail_url, kwargs={'pk': 2})
        data = {
            'username': 'username4@gmail.com',
            'first_name': 'Firstname4',
            'last_name': 'Secondname4',
            'password': 'password',
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['username'], 'test2@example.com')

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['username'], 'username4@gmail.com')
