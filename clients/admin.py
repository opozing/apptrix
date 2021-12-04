from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """
    Отображает нужные поля в админке
    """
    list_display = ('avatar', 'sex', 'first_name', 'last_name', 'email',
                    'password')


admin.site.register(CustomUser, CustomUserAdmin)
