from django.contrib import admin
from django_neomodel import admin as neo_admin

from .models import PostgresProduct
from .neomodels import NeoProduct as NeoProduct

admin.site.register(PostgresProduct)


class NeoProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


neo_admin.register(NeoProduct, NeoProductAdmin)
