'''Importing necessary modules and classes'''
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls configuration class."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
