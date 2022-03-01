from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    class Meta:
        fields = '__all__'


@admin.register(Mail)
class UserAdmin(admin.ModelAdmin):

    class Meta:
        fields = '__all__'