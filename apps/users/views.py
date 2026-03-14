from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.serializers import LoginSerializer, ProfileSerializer, RegisterSerializer


@extend_schema(
    tags=['Authentication'],
    summary='Register a new user',
    request=RegisterSerializer,
    responses={201: RegisterSerializer, 400: OpenApiResponse(description='Validation error')},
)
class RegisterView(generics.CreateAPIView):
    '''
    View for user registration.
    '''
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=['Authentication'],
    summary='Login and get JWT tokens',
    responses={200: LoginSerializer},
)
class LoginView(TokenObtainPairView):
    '''
    View for user login and obtaining JWT tokens.
    '''
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=['Authentication'],
    summary='Refresh JWT access token',
)
class RefreshTokenView(TokenRefreshView):
    '''
    View for refreshing JWT access token.
    '''
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    '''
    View for retrieving and updating the current user's profile.
    '''
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=['Authentication'],
        summary='Get current user profile',
        responses={200: ProfileSerializer},
    )
    def get(self, request, *args, **kwargs):
        '''
        Retrieve the current user's profile.
        '''
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Authentication'],
        summary='Update current user profile',
        request=ProfileSerializer,
        responses={200: ProfileSerializer, 400: OpenApiResponse(description='Validation error')},
    )
    def patch(self, request, *args, **kwargs):
        '''
        Update the current user's profile.
        '''
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
