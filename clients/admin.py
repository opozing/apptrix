from django.contrib import admin
from .models import CustomUser, Match


class CustomUserAdmin(admin.ModelAdmin):
    """
    Отображает поля модели CustomUser в админке.
    """
    list_display = ('pk', 'avatar', 'sex', 'first_name', 'last_name', 'email',
                    'password')


class MatchAdmin(admin.ModelAdmin):
    """
    Отображает поля модели Match в админке.
    """
    list_display = ('pk', 'user', 'user_like')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Match, MatchAdmin)
