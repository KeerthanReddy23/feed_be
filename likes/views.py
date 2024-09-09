from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Likes
from .serializers import Likesserializer

@api_view(['POST'])
def like(request):
    serializer = Likesserializer(data=request.data)
    if serializer.is_valid():
        like = request.data.get('like')
        if like.lower() == 'like':
            serializer.save()
            res = {'status': 'User Liked Story'}
            return Response(res, status=status.HTTP_201_CREATED)
        elif like.lower() == 'unlike':
            userid = request.data.get('userid')
            postid = request.data.get('postid')
            likedpost = Likes.objects.filter(userid=userid,postid=postid).first()
            likedpost.delete()
            res = {'status': 'User Unliked Story'}
            return Response(res, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['get'])
def post_likes(request,postid):
    try:
        total_likes = Likes.objects.filter(postid=postid).count()
        likes = Likes.objects.filter(postid=postid)
        users = []
        for like in likes:
            users.append(like.userid.pk)
        res = {
            'users' : users,
            'likes' : total_likes,
        }
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {'status': 'Error'}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)