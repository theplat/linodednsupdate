from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Initialize admin user if no users exist'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = 'admin'
            password = 'temppassword'
            try:
                admin = User.objects.create_superuser(
                    username=username,
                    email='admin@example.com',
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'Admin user created - username: {username}'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR('Admin user already exists'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists')) 