from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    domain_id = models.IntegerField(help_text="Linode Domain ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DNSRecord(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='records')
    name = models.CharField(max_length=255, help_text="Subdomain name (e.g., 'www' for www.example.com)")
    current_value = models.CharField(max_length=255, help_text="Current IP address")
    record_id = models.IntegerField(help_text="Linode Record ID")
    last_updated = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('domain', 'name')

    def __str__(self):
        return f"{self.name}.{self.domain.name}"
