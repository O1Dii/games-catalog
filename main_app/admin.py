from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserModel


admin.site.register(UserModel, UserProfileAdmin)
