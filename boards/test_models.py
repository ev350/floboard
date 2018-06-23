from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Board, Column, Label, Card, Comment


class BoardModelTest(TestCase):
    """This class defines the test suite for the Board model."""

    def setUp(self):
        self.user = self.setup_user()

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_can_create_a_board(self):
        board = Board(title='Test Board', created_by=self.user)
        old_count = Board.objects.count()
        board.save()
        new_count = Board.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_board_must_have_title(self):
        board = Board(created_by=self.user)
        try:
            board.save()
        except ValidationError:
            self.assertTrue(True)


class ColumnModelTest(TestCase):
    """This class defines the test suite for the Column model."""

    def setUp(self):
        self.user = self.setup_user()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_can_create_a_column(self):
        column = Column(board=self.board, title='Backlog', position=1)
        old_count = Column.objects.count()
        column.save()
        new_count = Column.objects.count()
        self.assertNotEqual(old_count, new_count)


class LabelModelTest(TestCase):
    """This class defines the test suite for the Label model."""

    def setUp(self):
        self.user = self.setup_user()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_can_create_a_label(self):
        label = Label(board=self.board, title='Feature', color='#00FF00')
        old_count = Label.objects.count()
        label.save()
        new_count = Label.objects.count()
        self.assertNotEqual(old_count, new_count)


class CardModelTest(TestCase):
    """This class defines the test suite for the Card model."""

    def setUp(self):
        self.user = self.setup_user()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        self.column = Column(board=self.board, title='Backlog', position=1)
        self.column.save()

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_can_create_a_card_wo_column(self):
        card = Card(board=self.board, title='Test Card', description='Test Card description.', created_by=self.user)
        old_count = Card.objects.count()
        card.save()
        new_count = Card.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_can_create_a_card_w_column(self):
        card = Card(board=self.board, column=self.column, title='Test Card', description='Test Card description.',
                    created_by=self.user)
        old_count = Card.objects.count()
        card.save()
        new_count = Card.objects.count()
        self.assertEqual(card.column, self.column)
        self.assertNotEqual(old_count, new_count)


class CommentModelTest(TestCase):
    """This class defines the test suite for the Comment model."""

    def setUp(self):
        self.user = self.setup_user()
        self.board = Board(title='Test Board', created_by=self.user)
        self.board.save()
        self.column = Column(board=self.board, title='Backlog', position=1)
        self.column.save()
        self.card = Card(board=self.board, title='Test Card', description='Test Card description.',
                         created_by=self.user)
        self.card.save()

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_can_create_a_comment(self):
        comment = Comment(card=self.card, message='Test Card comment.', created_by=self.user)
        old_count = Comment.objects.count()
        comment.save()
        new_count = Comment.objects.count()
        self.assertNotEqual(old_count, new_count)
