from urllib import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
from notifications.models import Notification
from notifications.serializers import NotificationSerializer,Notification2Serializer
from rest_framework.decorators import api_view
from django.conf import settings
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
        


def send_fcm_notification(device_token, title, body, data=None):
    # Firebase server key
    server_key = settings.FCM_DJANGO_SETTINGS['FCM_SERVER_KEY']
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + server_key,
    }
    payload = {
        'to': device_token,
        'notification': {
            'title': title,
            'body': body,
        },
        'data': data if data else {}
    }
    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(payload))
    return response.json()


@api_view(['POST'])
def notify_user(request):
    serializer = Notification2Serializer(data=request.data)
    if serializer.is_valid():
        title = serializer.validated_data['title']
        body = serializer.validated_data['body']
        data = serializer.validated_data.get('data', {})
        device_token = request.data.get('device_tokens')

        if not device_token:
            return Response({'error': 'Device token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        response = send_fcm_notification(device_token, title, body, data)
        return Response(response, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)