from django.db import models

class Board(models.Model) :
    # 글번호 
    no = models.AutoField(primary_key=True, auto_created=1000)
    # 제목 
    title = models.CharField(max_length=100)
    # 내용 
    contents = models.TextField(null=True, blank=True)
    # 작성자
    author = models.ForeignKey(
        "users.User", 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='boards'
    )
    # 파일
    loaded_file = models.FileField(null=True, blank=True) 
    # 이미지 링크 
    image_url = models.URLField(default='')
    # 등록일
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정일 
    modified_at = models.DateTimeField(auto_now=True)
    