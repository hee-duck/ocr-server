from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.http.response import HttpResponse
from django.conf import settings
from pyuploadcare import Uploadcare, File
from .models import Board
from .serializers import BoardSerializer

import json
from PIL import Image
from django.db import models

def say_hello(request) :
    return render(request, "index.html", {
        "data" : Board.objects.all()
    }) 

# @api_view(['GET', 'POST'])
# def get_board_all(request) :
#     boards = Board.objects.all()
#     # -> Board를 JSON으로 형변환 (Serializer)
#     serializer = BoardSerializer(boards, many=True)
#     return Response(serializer.data)

class Boards(APIView) :
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request) :
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request) :
        serializer = BoardSerializer(data=request.data)

        if serializer.is_valid() :
            board = serializer.save() # create() 메소드를 호출하게 됨 

            if board.loaded_file and board.loaded_file.size < settings.FILE_SIZE_LIMIT :
                uploadcare = Uploadcare(public_key=settings.UC_PUBLIC_KEY, secret_key=settings.UC_SECRET_KEY)
                with open(board.loaded_file.path, 'rb') as file_object:
                    ucare_file = uploadcare.upload(file_object)
                    image_url = f"https://ucarecdn.com/{ucare_file.uuid}/"
                    board.image_url = image_url

            board.author = request.user
            board.save()
            return redirect(f'/board/{board.pk}')

        return Response(serializer.errors)


class BoardDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            board = Board.objects.get(pk=pk)
            return board
        except Board.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk):
        board = self.get_object(pk)

        if not board.author == request.user:
            raise PermissionDenied

        serializer = BoardSerializer(instance=board, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        board = self.get_object(pk)

        if not board.author == request.user:
            raise PermissionDenied

        board.delete()
        return Response({})

    def post(self, request, pk):
        board = self.get_object(pk)

        # 이미지 파일 업로드 처리
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            if image_file.size > settings.FILE_SIZE_LIMIT:
                raise ValidationError({'error': '이미지 파일 크기가 제한을 초과했습니다.'})

            # 이미지 파일을 업로드하여 URL 획득
            uploadcare = Uploadcare(public_key=settings.UC_PUBLIC_KEY, secret_key=settings.UC_SECRET_KEY)
            ucare_file = uploadcare.upload(image_file)
            image_url = f"https://ucarecdn.com/{ucare_file.uuid}/"
            board.loaded_file = image_url

            # 언어 설정
            langs = request.data.getlist('lang')

            # 텍스트 추출
            text = ''
            for lang in langs:
                text += convert_image_to_text(lang, image_file)

            # 텍스트가 빈 문자열이 아닌 경우 JSON 추출
            if text:
                board.ocr_result = json.dumps({'data': text})

            board.save()
            serializer = BoardSerializer(board)
            return Response(serializer.data)

        return Response({'error': '이미지 파일을 찾을 수 없습니다.'})