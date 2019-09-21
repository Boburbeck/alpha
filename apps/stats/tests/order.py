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
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 4)
        self.assertEqual(response.data[0]['first_name'], 'Firstname4')
        self.assertEqual(response.data[0]['sales'], '155900.000000000')

    # def test_create(self):
    #     url = reverse(self.list_url)
    #     response = self.client.post(url, data=self.data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['total_price'], '63000.000000000')
    #     self.assertEqual(response.data['id'], 7)
    #
    # def test_crate_fail(self):
    #     data = {"price": "1500"}
    #     url = reverse(self.list_url)
    #     response = self.client.post(url, data=data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['product'][0], 'This field is required.')
    #
    #     data = {"product": 1}
    #     url = reverse(self.list_url)
    #     response = self.client.post(url, data=data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['price'][0], 'This field is required')
    #
    # def test_is_active(self):
    #     url = reverse(self.detail_url, kwargs={'pk': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    #     self.assertEqual(response.data['id'], 1)
    #     self.assertEqual(response.data['is_active'], True)
    #
    #     url = reverse(self.list_url)
    #     response = self.client.post(url, data=self.data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #     url = reverse(self.detail_url, kwargs={'pk': 1})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
    #     self.assertEqual(response.data['id'], 1)
    #     self.assertEqual(response.data['is_active'], False)
    #
    # def test_delete(self):
    #     url = reverse(self.detail_url, kwargs={'pk': 5})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
