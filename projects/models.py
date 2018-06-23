from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """Represents a project."""

    title = models.CharField(max_length=255, null=False)


class Team(models.Model):
    """Represents a team."""

    name = models.CharField(max_length=255, null=False)
    members = models.ManyToManyField(User, through='Membership')
    projects = models.ManyToManyField(Project, related_name='team_projects')


class Role(models.Model):
    """Represents a role."""

    title = models.CharField(max_length=255, null=False)
    description = models.TextField()


class Membership(models.Model):
    """Represents a user's membership of a team."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
