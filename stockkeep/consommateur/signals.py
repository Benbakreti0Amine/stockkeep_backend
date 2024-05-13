from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import BonDeCommandeInterne
from magasinier.middleware import current_request

@receiver(post_save, sender=BonDeCommandeInterne)
def send_notification_on_bci(sender, instance, created, **kwargs):
    if not created:  # Check if the instance is being updated
        if instance.status == 'Created succesfully':
            user = instance.Consommateur_id
            Notification.objects.get_or_create(
                recipient=user,
                message=f"{user.username} from {user.structure}.",
                role = user.role
            )
        elif instance.status == 'Consulted by the responsable':
            user = current_request().user
            Notification.objects.get_or_create(
                recipient=user,
                message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                role = user.role
            )
        elif instance.status == 'Consulted by the director':
            user = current_request().user
            Notification.objects.get_or_create(
                recipient=user,
                message=f"{user.username} has validated the internal order ID {instance.id}.",
                role = user.role
            )
