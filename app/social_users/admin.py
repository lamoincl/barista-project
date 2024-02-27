from django.contrib import admin
from django_neomodel import admin as neo_admin

from .models import PostgresUser
from .neomodels import NeoUser

admin.site.register(PostgresUser)


class NeoUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


neo_admin.register(NeoUser, NeoUserAdmin)
