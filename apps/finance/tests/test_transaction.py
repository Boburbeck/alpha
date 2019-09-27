# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class TransactionCRUDTest(APITestCase):
    fixtures = [
        'users.yaml',
        'categories.yaml',
        'stocks.yaml',
        'clients.yaml',
        'products.yaml',
        'product_balances.yaml',
        'sold_costs.yaml',
        'order_products.yaml',
        'orders.yaml',
        'transactions.yaml',
    ]
    data = dict(income_amount="70000", spent_amount="0", client=1, order=1, stock=1, transaction_type="1")

    list_url = 'finance:transaction-list'
    detail_url = 'finance:transaction-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 8)

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['income_amount'], '70000.000000000')
