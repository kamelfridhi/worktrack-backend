"""
Django management command to create a superuser if one doesn't exist.
This is useful for automated deployments where shell access is not available.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the superuser (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@zeenalzein.com',
            help='Email for the superuser (default: admin@zeenalzein.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=None,
            help='Password for the superuser (if not provided, uses ADMIN_PASSWORD env var or generates a random one)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password'] or os.environ.get('ADMIN_PASSWORD')

        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists. Skipping creation.')
            )
            return

        # If no password provided, generate a random one
        if not password:
            import secrets
            password = secrets.token_urlsafe(16)
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  No password provided. Generated random password: {password}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  IMPORTANT: Save this password or set ADMIN_PASSWORD env variable!'
                )
            )

        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superuser "{username}" created successfully!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {str(e)}')
            )

