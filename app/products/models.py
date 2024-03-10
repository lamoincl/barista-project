from random import randrange
import factory

from django.db import models


class PostgresProduct(models.Model):
    name = models.CharField(verbose_name="Name")
    price = models.PositiveIntegerField(verbose_name="Prix")


class PostgresProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PostgresProduct

    name = factory.Faker("word")
    price = factory.LazyFunction(lambda: randrange(1, 1500))
