from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# There’s also a get_list_or_404() function, which works just as get_object_or_404()
# except using filter() instead of get(). It raises Http404 if the list is empty

# from .models import Question
from . import models

# Create your views here.
def index(request):
    latest_question_list = models.Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # try:
    #     question = models.Question.objects.get(pk = question_id)
    # except models.Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, models.Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
             {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
            )
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
