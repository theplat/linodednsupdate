from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from django.conf import settings
import base64


class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    domain_id = models.IntegerField(help_text="Linode Domain ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DNSRecord(models.Model):
    RECORD_TYPES = [
        ('A', 'A Record'),
        ('AAAA', 'AAAA Record'),
    ]

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='records')
    name = models.CharField(max_length=255, help_text="Subdomain name (e.g., 'www' for www.example.com)")
    record_type = models.CharField(max_length=4, choices=RECORD_TYPES, default='A')
    ttl = models.IntegerField(default=300, validators=[MinValueValidator(300)],
                            help_text="Time To Live in seconds (minimum 300)")
    current_value = models.CharField(max_length=255, help_text="Current IP address")
    record_id = models.IntegerField(help_text="Linode Record ID")
    last_updated = models.DateTimeField(auto_now=True)
    update_interval = models.IntegerField(default=300, validators=[MinValueValidator(60)],
                                        help_text="Update interval in seconds (minimum 60)")
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('domain', 'name', 'record_type')

    def __str__(self):
        return f"{self.name}.{self.domain.name} ({self.record_type})"


class UpdateLog(models.Model):
    record = models.ForeignKey(DNSRecord, on_delete=models.CASCADE, related_name='updates')
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.record} - {self.old_value} -> {self.new_value} ({self.updated_at})"


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
