from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.user_management import PayrollRoleManager


class Command(BaseCommand):
    help = 'Setup default roles and create super admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a super admin user'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username for super admin'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for super admin'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for super admin'
        )

    def handle(self, *args, **options):
        # Initialize roles
        self.stdout.write('Initializing system roles...')
        try:
            PayrollRoleManager.create_default_groups()
            self.stdout.write(
                self.style.SUCCESS('Successfully created default roles and permissions')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating roles: {str(e)}')
            )
            return

        # Create super admin if requested
        if options['create_superuser']:
            username = options.get('username')
            email = options.get('email')
            password = options.get('password')
            
            if not username:
                username = input('Username: ')
            if not email:
                email = input('Email: ')
            if not password:
                import getpass
                password = getpass.getpass('Password: ')
            
            try:
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f'User "{username}" already exists')
                    )
                else:
                    user = PayrollRoleManager.create_super_admin(
                        username=username,
                        email=email,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created super admin: {username}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating super admin: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS('Role setup completed!')
        )
