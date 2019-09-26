# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class OrderStatisticsTest(APITestCase):
    fixtures = [
        'users.yaml',
        'categories.yaml',
        'stocks.yaml',
        'clients.yaml',
        'products.yaml',
        'sold_costs.yaml',
        'order_products.yaml',
        'orders.yaml',

    ]
    data = {
        "cashier": 2,
        "payment_type": "cash",
        "client": 2,
        "deliver": False,
        "order_number": 789456,
        "total_balance": "12000",
        "products": [
            {"product": 1, "amount": "3"},
            {"product": 2, "amount": "4"},
            {"product": 3, "amount": "2"},
        ]
    }

    list_url = 'stats:order-list'
    detail_url = 'main:order-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_by_order(self):
        url = '%ssub_by_order/' % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 6)
        self.assertEqual(response.data[0]['children_total'], '91000.000000000')
        self.assertEqual(response.data[0]['internal_total_price'], '91000.000000000')

        self.assertEqual(response.data[1]['id'], 5)
        self.assertEqual(response.data[1]['children_total'], '48500.000000000')
        self.assertEqual(response.data[1]['internal_total_price'], '48500.000000000')

    def test_by_cashier(self):
        url = '%ssub_by_cashier/' % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 4)
        self.assertEqual(response.data[0]['first_name'], 'Firstname4')
        self.assertEqual(response.data[0]['sales'], '155900.000000000')

    def test_by_single_cashier(self):
        url = '%ssub_by_cashier/?cashier=4' % reverse(self.list_url)
        response = self.client.get(url, )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 4)
        self.assertEqual(response.data[0]['first_name'], 'Firstname4')
        self.assertEqual(response.data[0]['sales'], '155900.000000000')

    def test_by_stock(self):
        url = '%ssub_by_stock/' % reverse(self.list_url)
        response = self.client.get(url, )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'Test Stock 1')
        self.assertEqual(response.data[0]['total'], '195400.000000000')

        self.assertEqual(response.data[1]['id'], 2)
        self.assertEqual(response.data[1]['name'], 'Test Stock 2')
        self.assertEqual(response.data[1]['total'], '146900.000000000')
