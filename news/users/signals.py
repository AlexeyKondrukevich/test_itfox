from django.contrib.auth import get_user_model

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


User = get_user_model()


@receiver(pre_save, sender=User)
def update_superuser_role(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.role = "admin"


@receiver(post_save, sender=User)
def update_user_role(sender, instance, **kwargs):
    if instance.is_admin:
        instance.is_staff = True
    else:
        instance.is_staff = False
