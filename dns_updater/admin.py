from django.contrib import admin
from .models import Domain, DNSRecord, UpdateLog


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain_id', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(DNSRecord)
class DNSRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'record_type', 'current_value', 'enabled', 'last_updated')
    list_filter = ('record_type', 'enabled', 'domain')
    search_fields = ('name', 'domain__name', 'current_value')
    ordering = ('domain', 'name')
    readonly_fields = ('last_updated',)


@admin.register(UpdateLog)
class UpdateLogAdmin(admin.ModelAdmin):
    list_display = ('record', 'old_value', 'new_value', 'updated_at', 'success')
    list_filter = ('success', 'record__domain', 'record__record_type')
    search_fields = ('record__name', 'record__domain__name', 'old_value', 'new_value')
    ordering = ('-updated_at',)
    readonly_fields = ('record', 'old_value', 'new_value', 'updated_at', 'success', 'error_message')
