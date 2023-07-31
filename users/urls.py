from django.urls import path 
from .views import * 

urlpatterns = [
    path("", Users.as_view()),
    path("user/<int:pk>", UserDetail.as_view()),
    path("list", UserList.as_view()),
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
]