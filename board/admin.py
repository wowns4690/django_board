from django.contrib import admin
from .models import Board
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.

@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'contents',
        'writer',
        'board_name',
        'hits',
        'write_dttm',
        'update_dttm'
    )
    list_display_links = list_display
