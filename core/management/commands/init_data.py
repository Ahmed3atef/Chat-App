import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from chat.models import ChatGroup


class Command(BaseCommand):
    help = 'Creates an initial superuser and a public chat group'

    def handle(self, *args, **options):
        User = get_user_model()

        # 1. Get credentials from .env (via os.environ)
        # Ensure these match the keys in your actual .env file
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'password123')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Missing environment variables for superuser credentials.'))
            return

        # 2. Create User (if not exists)
        user_exists = User.objects.filter(username=username).exists() or \
            User.objects.filter(email=email).exists()

        if user_exists:
            self.stdout.write(self.style.WARNING(
                f'User "{username}" or email "{email}" already exists. Skipping user creation.'))
            admin_user = User.objects.filter(username=username).first(
            ) or User.objects.filter(email=email).first()
        else:
            admin_user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created superuser: {username}'))

        # 3. Create Public Group (if not exists)
        # We use 'public-chat' as the unique ID and 'Public' as the display name
        public_group, created = ChatGroup.objects.get_or_create(
            group_name='public',
        )

        if created:
            # Optional: Add the admin to the public group members automatically
            public_group.members.add(admin_user)
            self.stdout.write(self.style.SUCCESS(
                'Successfully created group: Public Lobby'))
        else:
            self.stdout.write(self.style.WARNING(
                'Group "public-chat" already exists.'))
