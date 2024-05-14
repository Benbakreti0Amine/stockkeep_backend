from urllib import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class FetchUnreadNotifications(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        role = request.query_params.get('role')
        notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False )
        if role:
            notifications = notifications.filter(role__name=role)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FetchAllNotifications(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        role = request.query_params.get('role')
        notifications = Notification.objects.all()
        if role:
            notifications = notifications.filter(role__name=role)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAllNotificationsAsRead(APIView):
    def put(self, request):
        Notification.objects.filter(recipient=request.user).update(read_status=True)
        return Response(status=status.HTTP_200_OK)

class DeleteNotification(APIView):
    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)