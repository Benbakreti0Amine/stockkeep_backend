from rest_framework import serializers
from rest_framework.validators import ValidationError

from role.models import Role

from .models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset = Role.objects.all(), slug_field='name')

    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'first_name', 'last_name', 'is_active','password','role']

    def validate(self, attrs):
     email = attrs.get("email")  # Use get() method to safely retrieve email field

     if email:
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError("Email has already been used")

     return super().validate(attrs)


    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()


        return user
