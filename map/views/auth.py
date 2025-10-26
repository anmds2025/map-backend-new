from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password
from map.models.user import User
from map.serializers.auth import LoginSerializer
from map.utils.handle_response import handle_response


# =============================
# 🚀 LOGIN
# =============================
@swagger_auto_schema(
    method='post',
    operation_summary="Login user and get JWT tokens",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        },
    ),
    responses={
        200: 'Access and Refresh tokens along with user data',
        400: 'Invalid credentials'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return handle_response(
            data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': getattr(user, 'full_name', ''),
                }
            },
            message='Login successful',
            status_code=status.HTTP_200_OK
        )
    return handle_response(
        message=serializer.errors.get('non_field_errors', ['Invalid credentials'])[0],
        status_code=status.HTTP_400_BAD_REQUEST
    )


# =============================
# 🚪 LOGOUT
# =============================
@swagger_auto_schema(
    method='post',
    operation_summary="Logout user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist'),
        },
    ),
    responses={
        200: "Logout successful",
        400: "Invalid token or request"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return handle_response(message='Refresh token is required', status_code=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return handle_response(message='Logout successful', status_code=status.HTTP_200_OK)
    except Exception as e:
        return handle_response(message=str(e), status_code=status.HTTP_400_BAD_REQUEST)


# =============================
# 🧾 REGISTER
# =============================
@swagger_auto_schema(
    method='post',
    operation_summary="Register a new user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'name'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name'),
        },
    ),
    responses={201: 'User registered successfully', 400: 'Bad request or email already exists'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')

    if not email or not password or not name:
        return handle_response(
            message='Email, name and password are required',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return handle_response(
            message='Email already registered',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        email=email,
        name=name,
        password=make_password(password)
    )

    refresh = RefreshToken.for_user(user)
    return handle_response(
        data={
            'user': {'id': user.id, 'email': user.email, 'name': user.name},
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
        message='User registered successfully',
        status_code=status.HTTP_201_CREATED
    )