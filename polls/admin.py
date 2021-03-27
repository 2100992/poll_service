from django.contrib import admin

# Register your models here.

from polls import models


@admin.register(models.Poll)
class PollAdmin(admin.ModelAdmin):
    list_per_page = 20
    # list_display =


@admin.register(models.Query)
class QueryAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Response)
class ResponseAdmin(admin.ModelAdmin):
    list_per_page = 20
