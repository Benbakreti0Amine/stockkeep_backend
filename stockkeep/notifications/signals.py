from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from consommateur.models import BonDeCommandeInterne
from notifications.views import send_fcm_notification
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=BonDeCommandeInterne)
def notify_status_change(sender, instance, **kwargs):
    # Check if this is an update and not a new creation
    if not kwargs.get('created', False):
        print("ICI1")
        if instance.status == 'Consulted by the responsable':
            title = 'Status Changed'
            body = f'The status of your order has changed to {instance.status}'
                # Example: Get the user FCM token from the user profile or another model
            device_token = instance.user_id.token  # Adjust as per your model structure
            if device_token:
                print("ICI4")
                send_fcm_notification(device_token, title, body, data={"order_id": instance.pk})
        elif instance.status == 'Consulted by the director':
            title = 'Status Changed'
            body = f'The status of your order has changed to {instance.status}'
                # Example: Get the user FCM token from the user profile or another model
            device_token = instance.user_id.token  # Adjust as per your model structure
            if device_token:
                print("ICI3")
                send_fcm_notification(device_token, title, body, data={"order_id": instance.pk})