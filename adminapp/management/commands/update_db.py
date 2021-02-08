from django.core.management.base import BaseCommand
from authapp.models import User
from authapp.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            UserProfile.objects.create(user=user)

