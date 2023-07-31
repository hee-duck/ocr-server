from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin) :
    list_display = [
        "no",
        "title",
        "author",
        "created_at",
    ]

    list_filter = [
        "author",
        "created_at",
    ]

    sortable_by = [
        "created_at",
        "modified_at",

    ]
