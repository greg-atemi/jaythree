from django.test import TestCase
from pos.models import Product

class MyModelTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        Product.objects.create(name='Object 1')
        Product.objects.create(name='Object 2')

    def test_model_creation(self):
        # Test if the objects were created correctly
        self.assertEqual(Product.objects.count(), 2)

    def test_model_query(self):
        # Test querying model instances
        queryset = Product.objects.filter(name='Object 1')
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().name, 'Object 1')