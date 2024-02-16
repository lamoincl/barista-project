from django.contrib import admin
from django_neomodel import admin as neo_admin

from .models import SGBDRProduct as SGBSDRProduct
from .neomodels import NeoProduct as NeoProduct

admin.site.register(SGBSDRProduct)


class NeoProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


neo_admin.register(NeoProduct, NeoProductAdmin)
