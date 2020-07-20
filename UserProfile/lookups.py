from django.contrib.auth.models import User

from selectable.base import ModelLookup
from selectable.registry import registry

class UserLookup(ModelLookup):
    model = User
    search_fields = ('username__icontains', )


registry.register(UserLookup)