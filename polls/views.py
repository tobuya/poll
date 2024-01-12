from django.conf import empty
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

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
    response = "You are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You are voting on question %s." % question_id)
