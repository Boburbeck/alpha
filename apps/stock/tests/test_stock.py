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


class StockEmployeeTest(APITestCase):
    fixtures = [
        'users.yaml',
        'stocks.yaml',
    ]
    data = dict(name="New/Updated Stock", address="New/Updated address", employees=[2, 3])

    list_url = 'stock:stock-list'
    detail_url = 'stock:stock-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['employees'][0]['first_name'], 'Firstname4')

    def test_detail_with_employees(self):
        url = reverse(self.detail_url, kwargs={'pk': 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employees'][0]['first_name'], 'Firstname4')

    def test_create_with_employees(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 3)
        self.assertEqual(response.data['name'], 'New/Updated Stock')
        self.assertEqual(response.data['employees'], [3, 2])


    def test_update_with_employees(self):
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employees'][0]['last_name'], "Secondname4")
        self.assertEqual(len(response.data['employees']), 3)
        self.assertEqual(response.data['name'], "Test Stock 2")

        response = self.client.put(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employees'][0], 3)
        self.assertEqual(len(response.data['employees']), 2)
        self.assertEqual(response.data['name'], "New/Updated Stock")

    def test_only_stock_employees(self):

        data = dict(employees=[2, 3])
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['employees']), 3)

        url = '%sadd_employees' % reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.put(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['employees']), 2)



    def test_delete(self):
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.delete(url, )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
