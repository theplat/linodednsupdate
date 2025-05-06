from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates an admin user if none exists'

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'temppassword')
                self.stdout.write('Admin user created - username: admin')
            else:
                self.stdout.write('Admin user already exists')
        except IntegrityError:
            self.stdout.write('Error creating admin user') 