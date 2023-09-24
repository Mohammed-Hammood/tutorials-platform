from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_token(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Token.objects.get_or_create(user=user)
