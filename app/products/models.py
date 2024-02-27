import factory
from decimal import Decimal

from django.db import models


class PostgresProduct(models.Model):
    name = models.CharField(verbose_name="Name")
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Prix")


class PostgresProductFactory(factory.Factory):
    class Meta:
        model = PostgresProduct

    name = factory.Faker("word")
    price = factory.Faker("random_number")
