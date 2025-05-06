from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings


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


class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encrypted_key = models.TextField()
    is_valid = models.BooleanField(default=False)
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"API Key for {self.user.username}"

    def set_key(self, key):
        """Encrypt and store the API key"""
        f = Fernet(settings.ENCRYPTION_KEY)
        self.encrypted_key = f.encrypt(key.encode()).decode()
        self.save()

    def get_key(self):
        """Decrypt and return the API key"""
        f = Fernet(settings.ENCRYPTION_KEY)
        return f.decrypt(self.encrypted_key.encode()).decode()
