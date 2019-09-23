# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class ProductBalanceCrudTest(APITestCase):
    fixtures = [
        'users.yaml',
        'categories.yaml',
        'products.yaml',
        'stocks.yaml',
        'product_balances.yaml',

    ]
    data = {
        "balance": "14",
        "defect": "1",
        "product": 2,
        "stock": 1,
    }

    list_url = 'main:product_balance-list'
    detail_url = 'main:product_balance-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

    def test_detail(self):
        url = reverse(self.detail_url, kwargs={'pk': 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], 5)
        self.assertEqual(response.data['balance'], '8.000000000')
        self.assertEqual(response.data['defect'], '2.000000000')

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['balance'], '14.000000000')
        self.assertEqual(response.data['defect'], '1.000000000')
        self.assertEqual(response.data['id'], 31)

    def test_update(self):
        url = reverse(self.detail_url, kwargs={'pk': 5})
        response = self.client.get(url)
        self.assertEqual(response.data['id'], 5)
        self.assertEqual(response.data['balance'], '8.000000000')

        response = self.client.put(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 5)
        self.assertEqual(response.data['balance'], '14.000000000')

    def test_delete(self):
        url = reverse(self.detail_url, kwargs={'pk': 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
