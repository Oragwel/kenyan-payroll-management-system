from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a test non-admin user for testing access restrictions'

    def handle(self, *args, **options):
        # Create a regular (non-admin) user
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpass123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists')
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=False,  # Not an admin
                is_superuser=False
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created non-admin user "{username}"')
            )
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(f'Admin status: {user.is_staff}')
