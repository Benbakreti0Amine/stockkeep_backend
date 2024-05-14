from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from magasinier.models import EtatInventaire
from magasinier.middleware import current_request

@receiver(post_save, sender=EtatInventaire)
def send_notification_on_etat(sender, instance, created, **kwargs):
    if not created: 
        if instance.etat == 'Approuved':
            user = current_request().user
            Notification.objects.get_or_create(
                recipient=user,
                message=f"{user.username} has approuved the inventory status N° {instance.id}.",
                role=user.role,
                titre = "Inventory status approuvement"
            )
