from rest_framework.serializers import ModelSerializer
from .models import Board
from users.serializers import UserOverviewSerializer

class BoardSerializer(ModelSerializer) :
    author = UserOverviewSerializer(read_only=True)

    class Meta :
        model = Board

        fields = "__all__"

        # depth = 1

        # fields = [
        #     "title",
        #     "contents",
        #     "author",
        # ]

        # exclude = [
        #     "modified_at",
        # ]