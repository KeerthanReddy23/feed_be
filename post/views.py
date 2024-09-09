from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post
from .serializers import Postserializer

@api_view(['POST'])
def create_post(request):
    serializer = Postserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['get'])
def all_posts(request):
    try:
        params = request.query_params
        if "userid" in params:
            posts = Post.objects.filter(userid=params.get('userid'))
        else:
            posts = Post.objects.all()
        serializer = Postserializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        res = {'status': 'Error'}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)