from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import BonDeCommandeInterne, Consommateur
from magasinier.middleware import current_request
from notifications.views import send_fcm_notification
from role.models import Role

@receiver(post_save, sender=BonDeCommandeInterne)
def send_notification_on_bci(sender, instance, created, **kwargs):
    # Check if a flag is set to avoid duplicate processing
    if hasattr(instance, '_notification_processed') and instance._notification_processed:
        return

    # Mark the instance as processed to prevent re-processing
    instance._notification_processed = True

    user = current_request().user
    print(instance.status)

    if instance.status == 'Created succesfully':
        consommateur = Consommateur.objects.get(user_ptr=instance.user_id)
        Notification.objects.get_or_create(
            recipient=instance.user_id,
            message=f"{instance.user_id.username} from {consommateur.structure}.",
            role=instance.user_id.role,
            titre="New internal order"
        )
    
    elif instance.status == 'Validated by the responsable':
        responsable_structure_role = Role.objects.get(name="responsable_structure")
        if not Notification.objects.filter(
            recipient=user,
            message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
            titre="Internal order validation by the Responsable",
            role=responsable_structure_role
        ).exists():
            Notification.objects.create(
                recipient=user,
                message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                titre="Internal order validation by the Responsable",
                role=responsable_structure_role,
                
            )
            print('responsable')
            title = 'Status Changed'
            body = f'The status of your order has changed to {instance.status}'
            if instance.user_id.token:
                Notification.objects.create(
                    recipient=instance.user_id,
                    message=body,
                    titre=title,
                    role=instance.user_id.role,
                )
                send_fcm_notification(instance.user_id.token, title, body, data={"order_id": instance.pk})
    
    else:
        directeur_role = Role.objects.get(name="directeur")
        if not Notification.objects.filter(
            recipient=user,
            message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
            titre="Internal order validation by the directeur",
            role=directeur_role
        ).exists():
            Notification.objects.create(
                recipient=user,
                message=f"Mr. {user.username} has validated the internal order ID {instance.id}.",
                titre="Internal order validation by the directeur",
                role=directeur_role,
                
            )
            print('director')
            title = 'Status Changed'
            body = f'The status of your order has changed to {instance.status}'
            if instance.user_id.token:
                Notification.objects.create(
                    recipient=instance.user_id,
                    message=body,
                    titre=title,
                    role=instance.user_id.role,
                )
                send_fcm_notification(instance.user_id.token, title, body, data={"order_id": instance.pk})
