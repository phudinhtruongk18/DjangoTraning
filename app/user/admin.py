"""Integrate with admin module."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import NomalUser


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')   # Các trường có gắn link dẫn đến trang detail
    readonly_fields = ('last_login', 'date_joined')     # Chỉ cho phép đọc
    ordering = ('-date_joined',)     # Sắp xếp theo chiều ngược

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # Bắt buộc phải khai báo
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(NomalUser, AccountAdmin)