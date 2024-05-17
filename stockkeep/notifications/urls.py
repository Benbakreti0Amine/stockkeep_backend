from django.urls import path

from .views import FetchAllNotifications, FetchUnreadNotifications, MarkAllNotificationsAsRead,DeleteNotification,SendNotificationView

app_name = 'notifications'

urlpatterns = [
    path('all/', FetchAllNotifications.as_view(), name='list'),
    path('unread/', FetchUnreadNotifications.as_view(), name='unread'),
    path('mark/', MarkAllNotificationsAsRead.as_view(), name='mark'),
    path('<int:notification_id>/', DeleteNotification.as_view(), name='delete_notification'),
    path('<send/', SendNotificationView.as_view(), name='delete_notification'),
]