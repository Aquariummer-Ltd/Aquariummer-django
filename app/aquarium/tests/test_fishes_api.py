from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Fish

from aquarium.serializers import FishSerializer


FISHES_URL = reverse('aquarium:fish-list')


class PublicFishesApiTests(TestCase):
    """Test the publicly available fishes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving fishes"""
        res = self.client.get(FISHES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFishesApiTests(TestCase):
    """Test the authorized user fishes API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'mymailaddress@hoge.huga',
            'lovepython'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_fishes(self):
        """Test retrieving fishes"""
        Fish.objects.create(user=self.user, name='ネオンテトラ')
        Fish.objects.create(user=self.user, name='金魚')

        res = self.client.get(FISHES_URL)

        fishes = Fish.objects.all().order_by('-name')
        serializer = FishSerializer(fishes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_fishes_limited_to_user(self):
        """Test that fishes returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@hoge.huga',
            'likepython'
        )
        Fish.objects.create(user=user2, name='オトシンクルス')
        fish = Fish.objects.create(user=self.user, name='ベタ')

        res = self.client.get(FISHES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], fish.name)

    def test_create_fish_successful(self):
        """Test creating a new fish"""
        payload = {'name': 'めだか'}
        self.client.post(FISHES_URL, payload)

        exists = Fish.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_fish_invalid(self):
        """Test creating a new fish with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(FISHES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
