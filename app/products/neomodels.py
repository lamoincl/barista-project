import factory
from django_neomodel import DjangoNode
from neomodel import StringProperty, FloatProperty, UniqueIdProperty


class NeoProduct(DjangoNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    price = FloatProperty()

    class Meta:
        app_label = 'products'
        verbose_name = "Neo4j Product"
        verbose_name_plural = "Neo4j Products"


class NeoProductFactory(factory.Factory):
    class Meta:
        model = NeoProduct

    name = factory.Faker("word")
    price = factory.Faker("random_number")
