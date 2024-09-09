from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Friends
from user.models import User
from .serializers import FriendSerializer

@api_view(['POST'])
def add_friend(request):
    user = request.user
    friend_id = request.data.get('friend_id')        
    try:
        friend = User.objects.get(userid=friend_id)
    except User.DoesNotExist:
        return Response({'error': 'Friend not found'}, status=status.HTTP_404_NOT_FOUND)    
    if Friends.objects.filter(user=user, friend=friend).exists():
        return Response({'error': 'Friendship already exists'}, status=status.HTTP_400_BAD_REQUEST)    
    data_user_to_friend = {
        'user': user.userid,
        'friend': friend.userid
    }    
    data_friend_to_user = {
        'user': friend.userid,
        'friend': user.userid
    }
    serializer_user_to_friend = FriendSerializer(data=data_user_to_friend)
    serializer_friend_to_user = FriendSerializer(data=data_friend_to_user)    
    if serializer_user_to_friend.is_valid() and serializer_friend_to_user.is_valid():
        serializer_user_to_friend.save()
        serializer_friend_to_user.save()
        return Response({
            'user_to_friend': serializer_user_to_friend.data,
            'friend_to_user': serializer_friend_to_user.data
        }, status=status.HTTP_201_CREATED)    
    return Response({
        'user_to_friend_errors': serializer_user_to_friend.errors,
        'friend_to_user_errors': serializer_friend_to_user.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def friends_list(request):
    user = request.user
    friends = Friends.objects.filter(user=user)
    serializer = FriendSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)