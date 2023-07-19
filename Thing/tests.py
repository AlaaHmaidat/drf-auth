from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Thing
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate

from rest_framework.test import APITestCase

from .models import Thing


class ThingTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(username = 'testuser1', password='testpass1')
        testuser1.save()

        testthing  = Thing.objects.create(name='testname1',owner=testuser1,desc='testdesc1')
        testthing .save()

    def setUp(self):
        self.client.login(username="testuser1", password="testpass1")

    def test_thing_model(self):
        thing1 = Thing.objects.get(id=1)
        actual_owner = str(thing1.owner)
        actual_name = str(thing1.name)
        actual_desc = str(thing1.desc)

        self.assertEqual(actual_owner,'testuser1')
        self.assertEqual(actual_name,'testname1')
        self.assertEqual(actual_desc,'testdesc1')

    def test_get_thing_list(self):
        url = reverse("Thing_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        things = response.data
        self.assertEqual(len(things), 1)
        self.assertEqual(things[0]["name"], "testname1")

    def test_get_thing_by_id(self):
        url = reverse("Thing_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        thing = response.data
        self.assertEqual(thing["name"], "testname1")

    def test_create_thing(self):
        url = reverse("Thing_list")
        data = {"owner": 1, "name": "testname1", "desc": "testdesc1"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        things = Thing.objects.all()
        self.assertEqual(len(things), 2)
        self.assertEqual(Thing.objects.get(id=2).name, "testname1")

    def test_update_thing(self):
        url = reverse("Thing_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "testname11",
            "desc": "testdesc11",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        thing = Thing.objects.get(id=1)
        self.assertEqual(thing.name, data["name"])
        self.assertEqual(thing.owner.id, data["owner"])
        self.assertEqual(thing.desc, data["desc"])

    def test_delete_thing(self):
        url = reverse("Thing_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        things = Thing.objects.all()
        self.assertEqual(len(things), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("Thing_list")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
