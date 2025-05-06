from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

def init_admin(sender, **kwargs):
    call_command('init_admin')

class DnsUpdaterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dns_updater'

    def ready(self):
        post_migrate.connect(init_admin, sender=self)
