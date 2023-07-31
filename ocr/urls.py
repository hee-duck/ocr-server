from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path("login", login),
    path("join", join),
    path("mypage", mypage),
    path("mypage/edit", user_update),
    path("board/write/", board_write),
    path("board/<int:pk>", board),
    path("board/<int:pk>/edit", board_update),
    path("boards", boards),
    path("ocr", OCR.as_view()),
]