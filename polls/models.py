'''Importing necessary modules and classes'''
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    """Class representing a question."""
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        """Function getting recent dates."""
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Class representing choice."""
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text
