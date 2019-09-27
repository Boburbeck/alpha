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
        self.assertEqual(response.data['results'][0]['total_balance'], '27.000000000')
        self.assertEqual(response.data['results'][0]['total_defect'], '4.000000000')
        self.assertEqual(response.data['results'][0]['total_sold'], '3.000000000')
        self.assertEqual(response.data['results'][0]['available'], '20.000000000')
        self.assertEqual(response.data['results'][0]['product'], '1')
        self.assertEqual(response.data['results'][0]['stock'], '1')

    def test_filter_by_stock(self):
        url = "%s?stock=1" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(response.data['results'][3]['total_balance'], '59.000000000')
        self.assertEqual(response.data['results'][3]['total_defect'], '9.000000000')
        self.assertEqual(response.data['results'][3]['total_sold'], '10.000000000')
        self.assertEqual(response.data['results'][3]['available'], '40.000000000')
        self.assertEqual(response.data['results'][3]['product'], '4')
        self.assertEqual(response.data['results'][3]['stock'], '1')

    def test_filter_by_product(self):
        url = "%s?product=4" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['total_balance'], '59.000000000')
        self.assertEqual(response.data['results'][0]['total_defect'], '9.000000000')
        self.assertEqual(response.data['results'][0]['total_sold'], '10.000000000')
        self.assertEqual(response.data['results'][0]['available'], '40.000000000')
        self.assertEqual(response.data['results'][0]['product'], '4')
        self.assertEqual(response.data['results'][0]['stock'], '1')

        self.assertEqual(response.data['results'][1]['total_balance'], '7.000000000')
        self.assertEqual(response.data['results'][1]['total_defect'], '3.000000000')
        self.assertEqual(response.data['results'][1]['available'], '4.000000000')
        self.assertEqual(response.data['results'][1]['product'], '4')
        self.assertEqual(response.data['results'][1]['stock'], '2')

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['balance'], '14.000000000')
        self.assertEqual(response.data['defect'], '1.000000000')
        self.assertEqual(response.data['id'], 31)
