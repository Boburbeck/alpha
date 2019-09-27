# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class ProductTest(APITestCase):
    fixtures = [
        'users.yaml',
        'categories.yaml',
        'products.yaml',
    ]
    data = {
        "category": 2,
        "name": "NEW/UPDATED PRODUCT",
        "code": "P-NEW",
    }

    list_url = 'main:product-list'
    detail_url = 'main:product-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 7)

    def test_detail(self):
        url = reverse(self.detail_url, kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], "Sub Category 1 Product 1")
        self.assertEqual(response.data['code'], "P-001")

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'NEW/UPDATED PRODUCT')

    def test_crate_fail(self):
        data = {}
        url = reverse(self.list_url)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['name'][0], 'This field is required.')

    def test_update(self):
        url = reverse(self.detail_url, kwargs={'pk': 1})
        response = self.client.put(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_delete(self):
        url = reverse(self.detail_url, kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
