from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Board, Column, Card, Comment, Label


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the User instance to JSON."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer to map the Comment instance to JSON."""

    def create(self, validated_data):
        card = self.context['card']
        comment = Comment.objects.create(
            card=card,
            **validated_data
        )
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'card', 'message', 'updated_at', 'created_by', 'updated_by')
        read_only_fields = ('id', 'board', 'card')


class LabelSerializer(serializers.ModelSerializer):
    """Serializer to map the Label instance to JSON."""

    def create(self, validated_data):
        board = self.context['board']
        label = Label.objects.create(
            board=board,
            **validated_data
        )
        return label

    class Meta:
        model = Label
        fields = ('id', 'board', 'title', 'color')
        read_only_fields = ('id', 'board')


class CardListSerializer(serializers.ModelSerializer):
    """Serializer to map the Card instance to JSON."""
    assignees = UserSerializer(many=True, read_only=True)
    labels = LabelSerializer(many=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = ('id', 'board', 'title', 'description', 'created_by', 'assignees', 'labels', 'comment_set')
        read_only_fields = ('id', 'board')


class CardCreateSerializer(serializers.ModelSerializer):
    """Serializer to map the Card instance to JSON."""
    assignees = UserSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    labels = PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())

    def create(self, validated_data):
        board = self.context['board']
        labels_data = validated_data.pop('labels')
        card = Card.objects.create(
            board=board,
            **validated_data
        )
        card.labels.set(labels_data)
        return card

    class Meta:
        model = Card
        fields = ('id', 'board', 'title', 'description', 'created_by', 'assignees', 'labels', 'comment_set')
        read_only_fields = ('id', 'board')


class ColumnSerializer(serializers.ModelSerializer):
    """Serializer to map the Column instance to JSON."""
    card_set = CardListSerializer(many=True, read_only=True)

    def create(self, validated_data):
        board = self.context['board']
        column = Column.objects.create(
            board=board,
            **validated_data
        )
        return column

    class Meta:
        model = Column
        fields = ('id', 'board', 'title', 'position', 'header_color', 'card_set')
        read_only_fields = ('id', 'board')


class BoardSerializer(serializers.ModelSerializer):
    """Serializer to map the Board instance to JSON."""
    column_set = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'created_by', 'column_set')

