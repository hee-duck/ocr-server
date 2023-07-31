from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import *

class Login(APIView) :
    def post(self, request) :
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        # Not None
        if user : 
            login(request, user)
            return Response({'login' : 'success'})
        else :
            return Response(status.HTTP_401_UNAUTHORIZED)

class Logout(APIView) :
    permission_classes = [IsAuthenticated]

    def post(self, request) :
        logout(request)
        # return Response({})
        return redirect("/api/v1/boards")

class UserList(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        if request.user.is_staff :
            users = User.objects.all()
            serializer = UserSerializer(instance=users, many=True)
            return Response(serializer.data)
        else :
            raise PermissionDenied

class Users(APIView) :
    def post(self, request) :
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid() :
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(UserViewSerializer(user).data)
        else :
            return Response(serializer.errors)

class UserDetail(APIView) :
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk) :
        try :
            user = User.objects.get(pk=pk)

            if not user == request.user :
                raise PermissionDenied
            
            return user 
        except User.DoesNotExist :
            raise NotFound

    def get(self, request, pk) :
        user = self.get_object(request, pk)
        serializer = UserViewSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk) :
        user = self.get_object(request, pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        
        if serializer.is_valid() : 
            user = serializer.save()

            if 'password' in request.data :
                user.set_password(user.password)
                user.save()

            return Response(serializer.data)
        else :
            return Response(serializer.errors)

    def delete(self, request, pk) :
        user = self.get_object(request, pk)
        user.delete() 
        return Response(status.HTTP_204_NO_CONTENT)