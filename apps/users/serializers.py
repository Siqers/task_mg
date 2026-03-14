from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer for User model, used for displaying user information.
    '''
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone', 'created_at')
        read_only_fields = ('id', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    '''Serializer for user registration, includes password field for creating new users.
    '''
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone', 'password', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        '''Create a new user with the provided validated data, ensuring the password is hashed.'''
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for user profile, used for updating user information without changing the password.'''
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')


class LoginSerializer(TokenObtainPairSerializer):
    '''Serializer for user login, extends TokenObtainPairSerializer to include additional user information in the token.'''
    @classmethod
    def get_token(cls, user):
        '''Override the get_token method to include additional user information in the token payload.'''
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        '''Override the validate method to include user information in the response data after successful authentication.'''
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
