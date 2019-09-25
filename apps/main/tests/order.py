# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class OrderCrudTest(APITestCase):
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

    ]
    data = {
        "cashier": 2,
        "payment_type": "cash",
        "client": 2,
        "deliver": False,
        "order_number": 789456,
        "products": [
            {"product": 1, 'stock': 1, "amount": "3"},
            {"product": 2, 'stock': 1, "amount": "4"},
            {"product": 3, 'stock': 1, "amount": "2"},
        ]
    }

    list_url = 'main:order-list'
    detail_url = 'main:order-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 6)
        self.assertEqual(response.data['results'][0]['id'], 6)
        self.assertEqual(response.data['results'][0]['total_price'], '91000.000000000')

    def test_detail(self):
        url = reverse(self.detail_url, kwargs={'pk': 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], 5)
        self.assertEqual(response.data['total_price'], '48500.000000000')

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '63000.000000000')

    def test_product_balance(self):
        product_balance_url = reverse('main:product_balance-list')
        response = self.client.get(product_balance_url)
        self.assertEqual(response.data['results'][0]['stock'], '1')
        self.assertEqual(response.data['results'][0]['product'], '1')
        self.assertEqual(response.data['results'][0]['total_sold'], '3.000000000')
        self.assertEqual(response.data['results'][0]['available'], "20.000000000")

        self.assertEqual(response.data['results'][7]['stock'], '1')
        self.assertEqual(response.data['results'][7]['product'], '3')
        self.assertEqual(response.data['results'][7]['total_sold'], '7.000000000')
        self.assertEqual(response.data['results'][7]['available'], "22.000000000")

        response = self.client.post(reverse(self.list_url), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '63000.000000000')

        response = self.client.get(product_balance_url)
        self.assertEqual(response.data['results'][0]['stock'], '1')
        self.assertEqual(response.data['results'][0]['product'], '1')
        self.assertEqual(response.data['results'][0]['total_sold'], '6.000000000')
        self.assertEqual(response.data['results'][0]['available'], "17.000000000")

        self.assertEqual(response.data['results'][7]['stock'], '1')
        self.assertEqual(response.data['results'][7]['product'], '3')
        self.assertEqual(response.data['results'][7]['total_sold'], '9.000000000')
        self.assertEqual(response.data['results'][7]['available'], "20.000000000")

    def test_not_enough_product(self):
        data = {
            "cashier": 2,
            "payment_type": "cash",
            "client": 2,
            "deliver": False,
            "order_number": 789456,
            "total_balance": "12000",
            "products": [
                {"product": 6, 'stock': 2, "amount": "3"},
            ]
        }
        url = reverse(self.list_url)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['products'][0]['product_balance'][0], 'There is not enough product in the stock')

    def test_create_with_delivery(self):
        data_with_delivery = {
            "cashier": 2,
            "payment_type": "cash",
            "client": 2,
            "deliver": True,
            'delivery_date': '2020-01-01',
            'delivery_price': "24000",
            "order_number": 7894567,
            "total_balance": "12000",
            "products": [
                {"product": 1, 'stock': 1, "amount": "3"},
                {"product": 2, 'stock': 1, "amount": "4"},
                {"product": 3, 'stock': 1, "amount": "2"},
            ]
        }
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '63000.000000000')

        response = self.client.post(url, data=data_with_delivery, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '87000.000000000')

    def test_order_update_status(self):
        url = reverse(self.detail_url, kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], '1')

        data = dict(status='2')
        url = "%sorder_status/" % reverse(self.detail_url, kwargs={"pk": 1})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], '2')

    def test_create_fail_same_order_number(self):
        self.test_create()

        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['order_number'][0], 'Order with this order number already exists.')

    def test_delete(self):
        url = reverse(self.detail_url, kwargs={'pk': 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
