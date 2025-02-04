from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Profile

class Command(BaseCommand):
    help = 'Create missing profiles for all users'

    def handle(self, *args, **options):
        User = get_user_model()
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))