from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .models import User
from .serializers import UserSerializer

def get_tokens(user):
    userinfo = {
        'userid' : user.userid,
        'email' : user.email,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'full_name' : user.full_name,
        'profile_pic' : user.profile_pic.url,
    }
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    refresh['user'] = userinfo
    access['user'] = userinfo
    return {
        'refresh': str(refresh),
        'access': str(access),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens(user)
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user:
        tokens = get_tokens(user)
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def find_user(request):
    try:
        search_term = request.query_params.get('search_term', '')
        if search_term:
            users = User.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search_term) | Q(email__icontains=search_term)
            )[:3]
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
