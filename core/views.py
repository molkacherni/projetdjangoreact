from cgitb import lookup
import profile
from .models import User,ProfileUser
from .serializers import ProfileSerializer, UserRegistrationSerializer,MyTokenObtainPairSerializer,UserListSerializer,UpdateUserSerializer,UpdatePasswordUserSerializer,UserProfileSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.decorators import action,parser_classes
from rest_framework.parsers import FormParser,MultiPartParser
from django.db.models import Q
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from django.core import serializers 
import os
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @action(methods=['POST'],detail=True)
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):

        if 'image' in request.data:
            user_profile = self.get_object()
            user_profile.image.delete()

            upload = request.data['image']

            user_profile.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': user_profile.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
class ListUserView(generics.ListAPIView,RetrieveModelMixin):
    # queryset = User.objects.filter(Q(role=3) | Q(role=2))
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserListSerializer

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer

    @action(methods=['POST'],detail=True)
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        if 'image' in request.data:
            user_profile = self.get_object()
            user_profile.image.delete()

            upload = request.data['image']

            user_profile.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': user_profile.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

class UpdateUserPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UpdatePasswordUserSerializer

class DeleteAccount(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request, pk, **kwargs):
        
        user=User.objects.filter(id=pk)
        user.delete()

        return Response({"result":"user delete"})

class ProfileListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
    queryset =ProfileUser.objects.all()


class UpdateProfile(APIView):
    permission_classes = (AllowAny,)
    def put(self, request, pk):
        user = ProfileUser.objects.get(id=pk)

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_204_NO_CONTENT)

        return Response(status=HTTP_400_BAD_REQUEST)
        
    @action(methods=['put'],detail=True)
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        if 'image' in request.data:
            user_profile = self.get_object()
            user_profile.image.delete()

            upload = request.data['image']

            user_profile.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': user_profile.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
