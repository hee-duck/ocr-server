from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer) :
    class Meta : 
        model = User 
        fields = "__all__"

class UserViewSerializer(ModelSerializer) :
    class Meta :
        model = User
        fields = [
            "username",
            "name",
            "email",
            "date_joined",
        ]

class UserOverviewSerializer(ModelSerializer) :
    class Meta : 
        model = User 
        fields = [
            "username",
            "name",
        ]