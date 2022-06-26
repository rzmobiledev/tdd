"""
Test for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingrediet_id):
    """create and return an ingredient detail url."""
    return reverse('recipe:ingredient-detail', args=[ingrediet_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class PublicIngredientAPITest(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test is required for retrieving ingredients."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test unauthenticated API request."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(
            user=self.user,
            name='Indomie'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Pizza'
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test list of ingredient is limited to authenticated users."""
        user2 = create_user(email='user2@example.com')
        Ingredient.objects.create(
            user=user2,
            name='Salt'
        )
        ingredients = Ingredient.objects.create(
            user=self.user,
            name='Pepper'
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)
        self.assertEqual(res.data[0]['id'], ingredients.id)

    def test_update_ingredient(self):
        """Updating an ingredients"""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Cliantro'
        )
        payload = {'name': 'Coriander'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_deleting_ingredients(self):
        """Test deleting ingredients."""
        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Lada Hitam'
        )
        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(
            user=self.user
        )
        self.assertFalse(ingredients.exists())
