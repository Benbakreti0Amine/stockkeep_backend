from django.db import models
from users.models import User
from role.models import Role

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='notification')