from django.contrib import admin

from .models import AccountBook


class AccountBookAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(AccountBook, AccountBookAdmin)
