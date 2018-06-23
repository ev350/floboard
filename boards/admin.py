from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .forms import LabelForm
from .models import Board, Column, Card, Comment, Label

# Default Admin SetUp
admin.site.register(Comment)

# Token Authentication
TokenAdmin.raw_id_fields = ('user',)


# InLines
class ColumnsInLine(admin.TabularInline):
    model = Column
    extra = 0


class CardsInLine(admin.TabularInline):
    model = Card
    extra = 0
    exclude = ['updated_at']


class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0


# Custom Admin Pages
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', '_columns', '_cards', '_comments')

    search_fields = ['title']

    inlines = [
        ColumnsInLine
    ]

    def _columns(self, obj):
        return Column.objects.filter(board=obj).count()

    def _cards(self, obj):
        columns = Column.objects.filter(board=obj)
        return Card.objects.filter(column__in=columns).count()

    def _comments(self, obj):
        columns = Column.objects.filter(board=obj)
        cards = Card.objects.filter(column__in=columns)
        return Comment.objects.filter(card__in=cards).count()


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'position', '_cards', '_comments')
    search_fields = ['title']

    form = LabelForm
    fieldsets = (
        (None, {
            'fields': ('title', 'board', 'position', 'header_color')
        }),
    )

    inlines = [
        CardsInLine
    ]

    def _cards(self, obj):
        return Card.objects.filter(column=obj).count()

    def _comments(self, obj):
        cards = Card.objects.filter(column=obj)
        return Comment.objects.filter(card__in=cards).count()


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    form = LabelForm
    fieldsets = (
        (None, {
            'fields': ('board', 'title', 'color')
        }),
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'short_description', 'display_assignees', 'display_labels', '_comments')

    search_fields = ['title']

    inlines = [
        CommentsInLine
    ]

    def _comments(self, obj):
        return Comment.objects.filter(card=obj).count()
