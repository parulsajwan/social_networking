from django.contrib.auth import get_user_model
from .models import FriendRequest
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    '''
    The CustomUserSerializer class is a serializer class in Django that is used to serialize and deserialize user data.
    This class provides validation for the email field, creates new user instances, and specifies the fields to be included in the serialized output.
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomLoginSerializer(serializers.Serializer):
    '''
    The CustomLoginSerializer class is a serializer class in Django that is used for validating user login credentials.
    It checks if the provided email and password are valid and returns the corresponding user if they are.
    '''
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email__iexact=email).first()
            if user and user.check_password(password):
                return {'user': user}
            raise serializers.ValidationError(
                {'error': 'Invalid email or password'})
        raise serializers.ValidationError(
            {'error': 'Email and password are required'})



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('__all__')
 

class GetFriendRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = FriendRequest
        fields = ['user']
    
    
    

