from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from role.models import RolePermission
from users.tokens import create_jwt_pair_for_user
from .models import User
from .serializers import NewPasswordSerializer, UserSerializer,ResetPasswordEmailSerializer,ResetPasswordSerializer,ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from django.contrib.auth import authenticate,get_user_model,update_session_auth_hash #bach t5lik dir login
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from urllib.parse import urljoin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
# Create your views here.


class ListCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    


class RetrieveUpdateDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
<<<<<<< HEAD
=======

>>>>>>> 070f3f362098294e1fd12e705439ae72304a8f54

class Activate_OR_Desactivate(APIView):
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active 
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)
    
class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = ResetPasswordEmailSerializer
    permission_classes = []

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        User1 = get_user_model()
        user = User1.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},request=request)
            print(reset_url)
            print(settings.FRONTEND_BASE_URL)
            reset_url2 = urljoin(settings.FRONTEND_BASE_URL, f"/resetpassword/{encoded_pk}/{token}/")

            print(reset_url2)
            # send the rest_link as mail to the user.
            subject = 'welcome to our app'
            message = f"Your password rest link: {reset_url2}" 
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email ]
 
            send_mail( subject, message, email_from, recipient_list )


            return Response(
                {"message": "check your email" },
                status=status.HTTP_200_OK,)
            # return Response(
            #     {"message": "check your email","encoded_pk": encoded_pk, "token": token },
            #     status=status.HTTP_200_OK,)
        else:
            return Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
)
        

class ResetPasswordAPI(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset success"},status=status.HTTP_200_OK,)

class PassChangeview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    update_session_auth_hash(request, user)  # To update session after password change

                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
                
                return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetriveByUsername(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            # Check if the old password is correct
            if not user.check_password(old_password):
                return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user) 

            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PermissionsCodenameView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_superuser:
            # Superuser has all permissions
            permissions = Permission.objects.all()
        else:
            # Retrieve permissions based on user's role
            permissions = RolePermission.objects.filter(role=request.user.role).values_list('auth_permission__codename', flat=True)
            # 'auth_permission__codename' specifies the field to be retrieved from the related Permission model
            # Setting flat=True ensures a flat list is returned instead of a list of tuples

        return Response({"permissions": permissions}, status=status.HTTP_200_OK)
