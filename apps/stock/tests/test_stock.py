# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class StockCRUDTest(APITestCase):
    fixtures = [
        'users.yaml',
        'stocks.yaml',
    ]
    data = dict(name="New/Updated Stock", address="New/Updated address")

    list_url = 'stock:stock-list'
    detail_url = 'stock:stock-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][1]['id'], 1)
        self.assertEqual(response.data['results'][1]['name'], 'Test Stock 1')

    def test_employee_count(self):
        url = '%semployee_count/' % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Test Stock 2')
        self.assertEqual(response.data[0]['staff'], '3.000000000')

        self.assertEqual(response.data[1]['name'], 'Test Stock 1')
        self.assertEqual(response.data[1]['staff'], '3.000000000')

        data = dict(stock=2, member=1, date_joined='2019-09-22', role='manager')
        response = self.client.post(reverse('stock:staff-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Test Stock 2')
        self.assertEqual(response.data[0]['staff'], '4.000000000')

        self.assertEqual(response.data[1]['name'], 'Test Stock 1')
        self.assertEqual(response.data[1]['staff'], '3.000000000')

    def test_detail(self):
        response = self.client.get(reverse(self.detail_url, kwargs={"pk": 2}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['name'], 'Test Stock 2')

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 3)
        self.assertEqual(response.data['name'], 'New/Updated Stock')

    def test_update(self):
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.put(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['name'], 'New/Updated Stock')

    def test_delete(self):
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.delete(url, )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
