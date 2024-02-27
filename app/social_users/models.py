import factory
from django.db import models


class PostgresUser(models.Model):
    first_name = models.CharField(verbose_name="First name")
    last_name = models.CharField(verbose_name="Last name")

    users = models.ManyToManyField(
        "self",
        verbose_name="Followed users",
        related_name="followers",
        symmetrical=False,
    )
    products = models.ManyToManyField(
        "products.PostgresProduct",
        verbose_name="Buyed products",
        related_name="buyers"
    )


class PostgresUserFactory(factory.Factory):
    class Meta:
        model = PostgresUser

    first_name = factory.Faker("last_name")
    last_name = factory.Faker("first_name")
