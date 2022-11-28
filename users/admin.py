from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phonenumber', 'is_staff', 'is_active',)
    list_filter = ('phonenumber', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phonenumber', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phonenumber', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phonenumber',)
    ordering = ('phonenumber',)


admin.site.register(CustomUser, CustomUserAdmin)