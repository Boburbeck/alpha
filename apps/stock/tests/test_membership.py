# Python


# Django
from django.urls import reverse
# Rest Framework

from rest_framework import status
from rest_framework.test import APITestCase

from main.tests.test_users import get_token


class MembershipCRUDTest(APITestCase):
    fixtures = [
        'users.yaml',
        'stocks.yaml',
        'memberships.yaml',
    ]
    data = dict(stock=2, member=4, date_joined='2019-09-22', role='manager')

    list_url = 'stock:staff-list'
    detail_url = 'stock:staff-detail'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + get_token())

    def test_list(self):
        response = self.client.get(reverse(self.list_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 6)

    def test_filter_by_date_joined_begin(self):
        url = "%s?date_joined_begin=2019-03-03" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

    def test_filter_by_date_joined_end(self):
        url = "%s?date_joined_end=2019-03-03" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_by_role(self):
        url = "%s?role=employee" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

        url = "%s?role=manager" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_stock(self):
        url = "%s?stock=1" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

        url = "%s?stock=2" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_by_member(self):
        url = "%s?member=2" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        url = "%s?member=1" % reverse(self.list_url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_detail(self):
        response = self.client.get(reverse(self.detail_url, kwargs={"pk": 2}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['member'], 2)

    def test_create(self):
        url = reverse(self.list_url)
        response = self.client.post(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stock'], 2)
        self.assertEqual(response.data['member'], 4)

    def test_stock_employees(self):
        url = reverse('stock:stock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results'][0]['employees']), 3)

        self.test_create()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results'][0]['employees']), 4)

    def test_update(self):
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['stock'], 1)
        self.assertEqual(response.data['member'], 2)

        response = self.client.put(url, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['stock'], 2)
        self.assertEqual(response.data['member'], 4)

    def test_delete(self):
        url = reverse(self.detail_url, kwargs={"pk": 2})
        response = self.client.delete(url, )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
