from django.contrib import admin

# from .models import Question, Choice
from .models import Question, Choice

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    """Model admin class"""
    fields = ["pub_date", "question_text"]
admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
