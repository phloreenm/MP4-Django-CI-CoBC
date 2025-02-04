from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Group

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        # Get or create the 'Clients' group
        clients_group, _ = Group.objects.get_or_create(name='Clients')
        user.groups.add(clients_group)
        return user