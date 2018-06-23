from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from boards.models import (
    Board, Column, Card, Comment, Label
)
from boards.serializers import (
    BoardSerializer, ColumnSerializer, CardListSerializer,
    CardCreateSerializer, CommentSerializer, LabelSerializer
)


class BoardList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.all()

        return queryset


class BoardDetail(APIView):
    """
    Retrieve, update or delete a Board instance.
    """

    def get_object(self, board_pk):
        try:
            return Board.objects.get(pk=board_pk)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, board_pk):
        board = self.get_object(board_pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, board_pk):
        board = self.get_object(board_pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_pk):
        board = self.get_object(board_pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ColumnList(generics.ListCreateAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

    def get_queryset(self):
        queryset = Column.objects.filter(board_id=self.kwargs['board_pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(pk=kwargs['board_pk'])

        post_data = {
            'title': request.data.get('title'),
            'position': request.data.get('position'),
        }
        serializer = ColumnSerializer(data=post_data, context={'board': board})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ColumnDetail(APIView):
    """
        Retrieve, update or delete a Column instance.
        """

    def get_object(self, board_pk, position):
        try:
            return Column.objects.get(board_id=board_pk, position=position)
        except Column.DoesNotExist:
            raise Http404

    def get(self, request, board_pk, position):
        column = self.get_object(board_pk, position)
        serializer = ColumnSerializer(column)
        return Response(serializer.data)

    def put(self, request, board_pk, position):
        column = self.get_object(board_pk, position)
        serializer = ColumnSerializer(column, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_pk, position):
        column = self.get_object(board_pk, position)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LabelList(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def get_queryset(self):
        queryset = Label.objects.filter(board_id=self.kwargs['board_pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(pk=kwargs['board_pk'])

        post_data = {
            'board': board.pk,
            'title': request.data.get('title'),
            'color': request.data.get('color'),
        }
        serializer = LabelSerializer(data=post_data, context={'board': board})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LabelDetail(APIView):
    """
        Retrieve, update or delete a Label instance.
        """

    def get_object(self, board_pk, label_pk):
        try:
            return Label.objects.get(pk=label_pk)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, board_pk, label_pk):
        label = self.get_object(board_pk, label_pk)
        serializer = LabelSerializer(label)
        return Response(serializer.data)

    def put(self, request, board_pk, label_pk):
        label = self.get_object(board_pk, label_pk)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_pk, label_pk):
        label = self.get_object(board_pk, label_pk)
        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardListSerializer

    def get_queryset(self):
        queryset = Card.objects.filter(board_id=self.kwargs['board_pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(pk=kwargs['board_pk'])

        post_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'created_by': request.data.get('created_by'),
            'assignees': request.data.get('assignees'),
            'labels': request.data.get('labels'),
        }
        serializer = CardCreateSerializer(data=post_data, context={'board': board})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CardDetail(APIView):
    """
    Retrieve, update or delete a Card instance.
    """

    def get_object(self, board_pk, card_pk):
        try:
            # board = Board.objects.get(pk=board_pk)
            # columns = Column.objects.filter(board=board)
            # TODO // Cards can exist outside of a column
            return Card.objects.get(
                pk=card_pk,
                # column__in=columns
            )
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, board_pk, card_pk):
        card = self.get_object(board_pk, card_pk)
        serializer = CardListSerializer(card)
        return Response(serializer.data)

    def put(self, request, board_pk, card_pk):
        card = self.get_object(board_pk, card_pk)
        serializer = CardCreateSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_pk, card_pk):
        card = self.get_object(board_pk, card_pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        try:
            card = Card.objects.get(pk=self.kwargs['card_pk'], board_id=self.kwargs['board_pk'])
            queryset = Comment.objects.filter(card=card)
        except (Card.DoesNotExist, Comment.DoesNotExist):
            raise Http404
        return queryset

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(pk=kwargs['board_pk'])
        card = Card.objects.get(pk=kwargs['card_pk'], board=board)

        post_data = {
            'message': request.data.get('message'),
            'created_by': request.data.get('created_by'),
        }
        serializer = CommentSerializer(data=post_data, context={'card': card})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """
    Retrieve, update or delete a Comment instance.
    """

    def get_object(self, board_pk, card_pk, comment_pk):
        try:
            card = Card.objects.get(pk=card_pk)
            return Comment.objects.get(pk=comment_pk, card=card)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, board_pk, card_pk, comment_pk):
        comment = self.get_object(board_pk, card_pk, comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, board_pk, card_pk, comment_pk):
        comment = self.get_object(board_pk, card_pk, comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_pk, card_pk, comment_pk):
        comment = self.get_object(board_pk, card_pk, comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
