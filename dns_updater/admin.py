from django.contrib import admin
from .models import Domain, DNSRecord, APIKey

admin.site.register(Domain)
admin.site.register(DNSRecord)
admin.site.register(APIKey)
