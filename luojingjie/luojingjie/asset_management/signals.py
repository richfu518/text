from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Asset, AssetLog

@receiver(post_save, sender=Asset)
def log_asset_save(sender, instance, created, **kwargs):
    action = '创建' if created else '修改'
    AssetLog.objects.create(asset=instance, user=instance.owner, action=action)

@receiver(post_delete, sender=Asset)
def log_asset_delete(sender, instance, **kwargs):
    AssetLog.objects.create(asset=instance, user=instance.owner, action='删除')