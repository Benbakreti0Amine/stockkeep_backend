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
        notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FetchAllNotifications(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAllNotificationsAsRead(APIView):
    def put(self, request):
        Notification.objects.filter(recipient=request.user).update(read_status=True)
        return Response(status=status.HTTP_200_OK)
    