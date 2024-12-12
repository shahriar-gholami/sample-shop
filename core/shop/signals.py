from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Announcement, Store

@receiver(post_save, sender=Announcement)
def update_store_has_notif(sender, instance, created, **kwargs):
    if created:
        Store.objects.all().update(has_notif=True)
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')