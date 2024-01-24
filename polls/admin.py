'''Importing necessary modules and classes'''
from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """
    Class specifying how the Choice model should be displayed
    inline with Question model.
    """
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """Model admin class"""
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["-pub_date"]
admin.site.register(Question, QuestionAdmin)
