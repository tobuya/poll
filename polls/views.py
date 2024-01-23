'''Importing necessary modules and classes'''
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

# There’s also a get_list_or_404() function, which works just as get_object_or_404()
# except using filter() instead of get(). It raises Http404 if the list is empty

from .models import Question, Choice

class IndexView(generic.ListView):
    """Class utilizing ListView generic view."""
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            choice__isnull=False,
            ).distinct().order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    """Class utilizing DetailView generic view."""
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            choice__isnull=False,
            ).distinct()

class ResultsView(generic.DetailView):
    """Class utilizing DetailView generic view."""
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            choice__isnull=False,
            ).distinct()

def vote(request, question_id):
    """Function for voting a question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
             {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
            )
    # selected_choice.votes += 1
    # Use F() to increment the votes atomically to avoid race conditions,
    # ensuring that each vote is counted correctly, even in a multi-user environment
    selected_choice.votes = F('votes') + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
