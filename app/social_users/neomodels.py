import factory

from django_neomodel import DjangoNode
from neomodel import StringProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom


class NeoUser(DjangoNode):
    uid = UniqueIdProperty()
    first_name = StringProperty()
    last_name = StringProperty()

    followed_users = RelationshipTo("NeoUser", "FOLLOW")
    followers = RelationshipFrom("NeoUser", "FOLLOW")
    products = RelationshipTo("products.neomodels.NeoProduct", "BUY")

    class Meta:
        app_label = 'social_users'


class NeoUserFactory(factory.Factory):
    class Meta:
        model = NeoUser

    first_name = factory.Faker("last_name")
    last_name = factory.Faker("first_name")
