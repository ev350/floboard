from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from boards.models import Board, Column, Label, Card, Comment


def setup_user():
    user_model = get_user_model()

    return user_model.objects.create_user(
        'test',
        email='testuser@test.com',
        password='test'
    )


class BoardAPIViewTest(TestCase):
    """Test suite for the Board API views."""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.user.save()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        # self.client.force_authenticate(self.user)

    def test_api_can_create_a_new_board(self):
        response = self.client.post(
            '/api/v1/boards/',
            {
                "title": "Test Board 2",
                "created_by": self.user.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.board.pk + 1)

    def test_api_can_update_a_board(self):
        response = self.client.put(
            '/api/v1/boards/{0}/'.format(self.board.pk),
            {
                "title": "Test Board Updated",
                "created_by": self.user.id  # TODO // Figure out whether it's possible not to provide all fields
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Board Updated')

    def test_api_can_delete_a_board(self):
        old_count = Board.objects.count()
        response = self.client.delete(
            '/api/v1/boards/{0}/'.format(self.board.pk)
        )
        new_count = Board.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_count, new_count)


class ColumnAPIViewTest(TestCase):
    """Test suite for the Column API views."""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.user.save()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        self.column = Column(board=self.board, title='Backlog', position=1)
        self.column.save()
        # self.client.force_authenticate(self.user)

    def test_api_can_create_a_new_column(self):
        response = self.client.post(
            '/api/v1/boards/{board_pk}/columns/'.format(board_pk=self.board.pk),
            {
                "title": "In Progress",
                "position": 2
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.column.pk + 1)  # TODO // Column tests should use the position

    def test_api_can_update_a_column(self):
        response = self.client.put(
            '/api/v1/boards/{board_pk}/columns/{position}/'.format(board_pk=self.board.pk, position=1),
            {
                "title": "Selected for Development",
                "position": 1
            }  # TODO // Figure out whether it's possible not to provide all fields
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Selected for Development')

    def test_api_can_delete_a_column(self):
        old_count = Column.objects.count()
        response = self.client.delete(
            '/api/v1/boards/{board_pk}/columns/{position}/'.format(board_pk=self.board.pk, position=1),
        )
        new_count = Column.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_count, new_count)


class LabelAPIViewTest(TestCase):
    """Test suite for the Label API views."""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.user.save()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        self.label = Label(board=self.board, title='Red Label', color='#FF0000')
        self.label.save()
        # self.client.force_authenticate(self.user)

    def test_api_can_create_a_new_label(self):
        response = self.client.post(
            '/api/v1/boards/{board_pk}/labels/'.format(board_pk=self.board.pk),
            {
                "title": "Green Label",
                "color": "#00FF00"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.label.pk + 1)

    def test_api_can_update_a_label(self):
        response = self.client.put(
            '/api/v1/boards/{board_pk}/labels/{label_pk}/'.format(board_pk=self.board.pk, label_pk=self.label.pk),
            {
                "title": "Blue Label",
                "color": "#0000FF"
            }  # TODO // Figure out whether it's possible not to provide all fields
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Blue Label')
        self.assertEqual(response.data['color'], '#0000FF')

    def test_api_can_delete_a_label(self):
        old_count = Label.objects.count()
        response = self.client.delete(
            '/api/v1/boards/{board_pk}/labels/{label_pk}/'.format(board_pk=self.board.pk, label_pk=self.label.pk),
        )
        new_count = Label.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_count, new_count)


class CardAPIViewSet(TestCase):
    """Test suite for the Card API views."""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.user.save()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        self.label = Label(board=self.board, title='Red Label', color='#FF0000')
        self.label.save()
        self.label2 = Label(board=self.board, title='Green Label', color='#00FF00')
        self.label2.save()
        self.card = Card(board=self.board, title='Test Card', description='Test Card description', created_by=self.user)
        self.card.save()
        # self.client.force_authenticate(self.user)

    def test_api_can_create_a_new_card(self):
        response = self.client.post(
            '/api/v1/boards/{board_pk}/cards/'.format(board_pk=self.board.pk),
            {
                "title": "Test Card",
                "description": "Test Card description.",
                "created_by": self.user.pk,
                "labels": [self.label.pk, self.label2.pk]
            },
            format='json'  # Explicit format: otherwise list is sent as str()
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.card.pk + 1)

    def test_api_can_update_a_card(self):
        response = self.client.put(
            '/api/v1/boards/{board_pk}/cards/{card_pk}/'.format(board_pk=self.board.pk, card_pk=self.card.pk),
            {
                "title": "Edited Test Card",
                "description": "Test Card description updated.",
                "created_by": self.user.pk,
                "labels": [self.label.pk, self.label2.pk]
            }  # TODO // Figure out whether it's possible not to provide all fields
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Edited Test Card')
        self.assertEqual(response.data['description'], 'Test Card description updated.')

    def test_api_can_delete_a_card(self):
        old_count = Card.objects.count()
        response = self.client.delete(
            '/api/v1/boards/{board_pk}/cards/{card_pk}/'.format(board_pk=self.board.pk, card_pk=self.card.pk),
        )
        new_count = Card.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_count, new_count)


class CommentAPIViewSet(TestCase):
    """Test suite for the Comment API views."""

    def setUp(self):
        self.client = APIClient()
        self.user = setup_user()
        self.user.save()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        self.label = Label(board=self.board, title='Red Label', color='#FF0000')
        self.label.save()
        self.label2 = Label(board=self.board, title='Green Label', color='#00FF00')
        self.label2.save()
        self.card = Card(board=self.board, title='Test Card', description='Test Card description', created_by=self.user)
        self.card.save()
        self.comment = Comment(card=self.card, message='Test message.', created_by=self.user)
        self.comment.save()
        # self.client.force_authenticate(self.user)

    def test_api_can_create_a_new_comment(self):
        response = self.client.post(
            '/api/v1/boards/{board_pk}/cards/{card_pk}/comments/'.format(board_pk=self.board.pk, card_pk=self.card.pk),
            {
                "message": "Test Message 2.",
                "created_by": self.user.pk,
            },
            format='json'  # Explicit format: otherwise list is sent as str()
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.comment.pk + 1)

    def test_api_can_update_a_comment(self):
        response = self.client.put(
            '/api/v1/boards/{board_pk}/cards/{card_pk}/comments/{comment_pk}/'.format(board_pk=self.board.pk,
                                                                                      card_pk=self.card.pk,
                                                                                      comment_pk=self.comment.pk),
            {
                "message": "Test Message 2 edited.",
                "updated_at": "2017-12-17 06:26:53",
                "created_by": self.user.pk,
                "updated_by": self.user.pk
            }  # TODO // Figure out whether it's possible not to provide all fields
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Test Message 2 edited.')
        self.assertEqual(response.data['updated_at'], "2017-12-17T06:26:53Z")
        self.assertEqual(response.data['updated_by'], self.user.pk)

    def test_api_can_delete_a_comment(self):
        old_count = Comment.objects.count()
        response = self.client.delete(
            '/api/v1/boards/{board_pk}/cards/{card_pk}/comments/{comment_pk}/'.format(board_pk=self.board.pk,
                                                                                      card_pk=self.card.pk,
                                                                                      comment_pk=self.comment.pk),
        )
        new_count = Comment.objects.count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(old_count, new_count)
