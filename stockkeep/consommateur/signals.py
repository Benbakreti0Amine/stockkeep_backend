from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import BonDeCommandeInterne, Consommateur
from magasinier.middleware import current_request
from notifications.views import send_fcm_notification

@receiver(post_save, sender=BonDeCommandeInterne)
def send_notification_on_bci(sender, instance, created, **kwargs):
    if not created:  # Only proceed if the instance is being updated
        user = current_request().user
        
        if instance.status == 'Created succesfully':
            consommateur = Consommateur.objects.get(user_ptr=instance.user_id)
            Notification.objects.get_or_create(
                recipient=instance.user_id,
                message=f"{instance.user_id.username} from {consommateur.structure}.",
                role=instance.user_id.role,
                titre="New internal order"
            )
        
        elif instance.status == 'Consulted by the responsable':
            if not Notification.objects.filter(
                recipient=user,
                message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                titre="Internal order validation by Res"
            ).exists():
                Notification.objects.create(
                    recipient=user,
                    message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                    role=user.role,
                    titre="Internal order validation by Res"
                )
                title = 'Status Changed'
                body = f'The status of your order has changed to {instance.status}'
                if user.token:
                    Notification.objects.create(
                        recipient=user,
                        message=body,
                        titre=title,
                        role=user.role,
                    )
                    send_fcm_notification(user.token, title, body, data={"order_id": instance.pk})
        
        elif instance.status == 'Consulted by the director':
            if not Notification.objects.filter(
                recipient=user,
                message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                titre="Internal order validation"
            ).exists():
                Notification.objects.create(
                    recipient=user,
                    message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                    role=user.role,
                    titre="Internal order validation"
                )
                title = 'Status Changed'
                body = f'The status of your order has changed to {instance.status}'
                if user.token:
                    Notification.objects.create(
                        recipient=user,
                        message=body,
                        titre=title,
                        role=user.role,
                    )
                    send_fcm_notification(user.token, title, body, data={"order_id": instance.pk})
