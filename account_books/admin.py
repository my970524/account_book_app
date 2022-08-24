from django.contrib import admin

from .models import AccountBook, AccountBookRecord


class AccountBookAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


class AccountBookRecordAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(AccountBook, AccountBookAdmin)
admin.site.register(AccountBookRecord, AccountBookRecordAdmin)
