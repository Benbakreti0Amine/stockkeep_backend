from django.urls import path

from .views import FetchAllNotifications, FetchUnreadNotifications, MarkAllNotificationsAsRead,DeleteNotification,notify_user,list_notifications

app_name = 'notifications'

urlpatterns = [
    path('all/', FetchAllNotifications.as_view(), name='list'),
    path('unread/', FetchUnreadNotifications.as_view(), name='unread'),
    path('mark/', MarkAllNotificationsAsRead.as_view(), name='mark'),
    path('<int:notification_id>/', DeleteNotification.as_view(), name='delete_notification'),
    path('send/', notify_user, name='send_notification'),
    path('notifications/', list_notifications, name='list_notifications'),
]