from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication


from social_networking_backend.serailizers import (
    CustomLoginSerializer,
    CustomUserSerializer,
    UserSerializer,
    FriendRequestSerializer,
    GetFriendRequestSerializer
)
from django.contrib.auth import get_user_model
from .models import FriendRequest
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class SignupView(APIView):
    '''
    The SignupView class is an API view that handles the signup functionality. It receives a POST request with user data, validates the data using the CustomUserSerializer,
    and creates a new user if the data is valid.
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Something went wrong', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    '''
    The LoginView class is an API view that handles the login functionality. It receives a POST request with user credentials, validates them using the CustomLoginSerializer,
    and returns a response indicating whether the login was successful or not.
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Something went wrong', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSearchPagination(PageNumberPagination):
    '''
    The UserSearchPagination class is a subclass of the PageNumberPagination class from the Django REST Framework.
    It provides pagination functionality for the search results of users in a social networking backend.
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchView(generics.ListAPIView):
    '''
    The UserSearchPagination class is a subclass of the PageNumberPagination class from the Django REST Framework.
    It provides pagination functionality for the search results of users in a social networking backend.
    '''
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        queryset = User.objects.all()
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            queryset = queryset.filter(email__icontains=search_query) | queryset.filter(
                username__icontains=search_query)
        return queryset


class RequestListSentView(generics.ListCreateAPIView):
    '''
    This code defines a class named RequestListSentView that is a subclass of generics.ListCreateAPIView.
    It is responsible for handling requests related to friend requests sent by a user in a social networking application.
    '''
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return FriendRequest.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status='A')
        serializer = GetFriendRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request,  *args, **kwargs):
        username = request.data.get('username', None)
        if username:
            try:
                if self.get_queryset().count() >= 3:
                    return Response({"error": "Can't send more than 3 requests"}, status=status.HTTP_400_BAD_REQUEST)
                friend_request_user = User.objects.filter(
                    username=username).first()
                if not friend_request_user:
                    return Response({"error": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                obj = self.get_queryset().filter(friends=friend_request_user.pk)
                if obj:
                    return Response({"error": "Request Already Sent"}, status=status.HTTP_400_BAD_REQUEST)
                data = {
                    'user': request.user.pk,
                    'friends': friend_request_user.pk
                }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    instance.request_count += 1
                    instance.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Username field is required."}, status=status.HTTP_400_BAD_REQUEST)


class RequestAcceptRejectView(generics.RetrieveUpdateAPIView):
    '''
    The RequestAcceptRejectView class is a view in a Django REST Framework API that handles accepting or rejecting friend requests.
    It retrieves friend requests where the current user is the recipient and the status is 'S'. It also allows listing and updating friend requests.
    '''
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return FriendRequest.objects.filter(friends=self.request.user, status='S')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GetFriendRequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            action = request.query_params.get('action')
            qs = FriendRequest.objects.filter(
                friends=request.user, user_id=user_id).first()
            if not qs:
                return Response({'error': 'Request not found'}, status=status.HTTP_400_BAD_REQUEST)
            if action in ['A', 'R']:
                data = {
                    'status': action
                }
                serializer = self.get_serializer(qs, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"error": "Action is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Something went wrong', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceivedRequestListView(generics.ListAPIView):
    '''
    The ReceivedRequestListView class is a view in a Django REST Framework API that is responsible for retrieving a list of friend requests received by a user.
    '''
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return FriendRequest.objects.filter(friends=self.request.user, status='S')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = GetFriendRequestSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Something went wrong', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
