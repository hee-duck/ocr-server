from django.urls import path
from .views import *

urlpatterns = [
    path('', Boards.as_view()),
    path('board/<int:pk>', BoardDetail.as_view()),
]