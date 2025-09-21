from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import RegisterSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment, Like
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q



User = get_user_model()

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message' : 'User has been registered successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response({'message' : 'User has been logged in successfully'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            httponly=True,
            value=access_token,
            secure=True,
            samesite='Strict',
        )
        login(request, user)
        return response

    return Response({'message' : 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'message': 'refresh token required'}, status=400)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        return Response({'message': 'invalid refresh token'}, status=400)
    
    response = Response({'message': 'Logged out.'}, status=200)
    response.delete_cookie('access_token')  # make sure name matches login cookie
    return response


#after logging in

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_view(request):
    if request.method == 'GET':
        following_users = request.user.following.all()
        following_posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
        other_posts = Post.objects.exclude(user__in=following_users).order_by('-created_at')
        posts = list(following_posts) + list(other_posts)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):
    try:
        posts = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'post does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method in ['PUT', 'DELETE'] and request.user != posts.user:
        return Response({'error' : 'not allowed'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = PostSerializer(posts)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = PostSerializer(posts, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        posts.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'post does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        comments = post.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_details(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'error': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'DELETE'] and request.user != comment.user:
        return Response({'error': 'not allowed'}, status=status.HTTP_403_FORBIDDEN)


    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_view(request, content_type, object_id):
    try:
        model = Post if content_type == 'post' else Comment
        obj = model.objects.get(id=object_id)
    except model.DoesNotExist:
        return Response({'message' : 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    content_type_obj = ContentType.objects.get_for_model(obj)
    like, created = Like.objects.get_or_create(
        user=request.user, object_id=obj.id, content_type=content_type_obj
    )
    if not created:
        like.delete()
        action = 'unliked'
    else:
        action = 'liked'
    
    like_count = Like.objects.filter(object_id=obj.id, content_type=content_type_obj).count()

    return Response({'action' : action, 'like_count' : like_count}, status=status.HTTP_200_OK)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return Response({'message' : 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_toggle(request, user_id):
    try: 
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message' : 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.data == target:
        return Response({'message' : 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user in target.followers.all():
        target.followers.remove(request.user)
        return Response({'message' : 'Unfollowed'}, status=status.HTTP_200_OK)
    else:
        target.followers.add(request.user)  
        return Response({'message' : 'Followed'}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_detail(request):

    try:
        user = request.user
    except User.DoesNotExist:
        return Response({'message' : 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    
    if request.method == 'GET':
        info = UserUpdateSerializer(user)
        return Response(info.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        info = UserUpdateSerializer(user, data=request.data, partial=True)
        if info.is_valid():
            info.save()
            return Response(info.data, status=status.HTTP_200_OK)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_view(request):
    query = request.GET.get('q','')
    if not query:
        return Response({'message' : 'Query param q required'}, status=status.HTTP_400_BAD_REQUEST)
    
    users = User.objects.filter(
        Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )
    users = users.exclude(id=request.user.id)
    info = UserSerializer(users, many=True)
    return Response(info.data, status=status.HTTP_200_OK)
