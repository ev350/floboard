from markdown import markdown

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import mark_safe
from django.template.defaultfilters import truncatechars

from rest_framework.authtoken.models import Token

from . import fields


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate a token for ever User created."""
    if created:
        Token.objects.create(user=instance)


class Board(models.Model):
    """Represents a board."""

    title = models.CharField(max_length=255, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.title)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Board, self).save(*args, **kwargs)


class Column(models.Model):
    """Represents a column."""

    # Parent
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    # Fields
    title = models.CharField(max_length=32)
    position = models.IntegerField(default=1, blank=False, null=False)
    header_color = fields.ColorField(default='#00FF00')

    def __str__(self):
        return '{0}: {1}'.format(self.board, self.title)


class Label(models.Model):
    """Represents a label."""

    # Parent
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    # Fields
    title = models.CharField(max_length=32)
    color = fields.ColorField(default='#FF0000')

    def __str__(self):
        return '{0}: {1}'.format(self.board, self.title)


class Card(models.Model):
    """Represents a card."""

    # Parent
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, null=True)

    # Fields
    title = models.CharField(max_length=255, null=False)
    description = models.TextField()

    assignees = models.ManyToManyField(User, blank=True, related_name='card_assignees')
    labels = models.ManyToManyField(Label, blank=True, related_name='card_labels')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)  # Blank for django-admin

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='card_created_by')

    def __str__(self):
        return '{0}: {1}'.format(self.column, self.title)

    # Functions to deal with Django Admin edit_list limitations
    def display_assignees(self):
        return ', '.join([user.username for user in self.assignees.all()])

    display_assignees.short_description = 'Assignees'
    display_assignees.allow_tags = True

    def display_labels(self):
        return ', '.join([label.title for label in self.labels.all()])

    display_labels.short_description = 'Labels'
    display_labels.allow_tags = True

    def short_description(self):
        return truncatechars(self.description, 100)


class Comment(models.Model):
    """Represents a comment."""

    # Parent
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    # Fields
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)  # Blank for django-admin

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_created_by')
    updated_by = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, null=True,
                                   related_name='comment_updated_by')

    def __str__(self):
        return truncatechars(self.message, 30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
