from django.contrib import admin
from .models import Domain, DNSRecord

admin.site.register(Domain)
admin.site.register(DNSRecord)
