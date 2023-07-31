from django.db import models
from django.contrib.auth.models import AbstractUser     # 장고 속성의 auth 패키지의 models

# DB와 소통할 수 있는 DB를 정의하는 공간

class User(AbstractUser) :                              # 장고의 모델을 이용해서 User 모델을 만든 상태
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    # 나만의 필드 추가
    name = models.CharField(max_length=200, default="", blank=True)
    # phone_number = models.IntegerField(max_length=200, default="", blank=True, unique=True)



