from django.contrib import admin

# from .models import Question, Choice
from . import models

# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Choice)
