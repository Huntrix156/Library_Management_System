"""
Management command: python manage.py setup_roles

Creates the three role groups (admin, librarian, member) and
optionally creates a superuser/admin account so you can log in
on a fresh database.

Usage:
    python manage.py setup_roles
    python manage.py setup_roles --create-admin --username boss --password secret123
"""

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create role groups (admin, librarian, member) and optionally a superuser.'

    def add_arguments(self, parser):
        parser.add_argument('--create-admin', action='store_true',
                            help='Also create an admin user')
        parser.add_argument('--username', default='admin',
                            help='Username for the admin account (default: admin)')
        parser.add_argument('--password', default='admin123',
                            help='Password for the admin account (default: admin123)')
        parser.add_argument('--email', default='admin@library.com',
                            help='Email for the admin account')

    def handle(self, *args, **options):
        # 1. Create the three groups
        for name in ('admin', 'librarian', 'member'):
            group, created = Group.objects.get_or_create(name=name)
            status = 'created' if created else 'already exists'
            self.stdout.write(f'  Group "{name}": {status}')

        self.stdout.write(self.style.SUCCESS('✓ Role groups ready.'))

        # 2. Optionally create an admin user
        if options['create_admin']:
            from accounts.models import CustomUser
            username = options['username']
            password = options['password']
            email    = options['email']

            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(
                    f'  User "{username}" already exists — skipping creation.'
                ))
            else:
                user = CustomUser.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    role='admin',
                    is_staff=True,
                )
                admin_group = Group.objects.get(name='admin')
                user.groups.add(admin_group)
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Admin user "{username}" created (password: {password}).\n'
                    f'  Log in at /accounts/login/ or /admin/'
                ))