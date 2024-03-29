'''Importing necessary modules and classes'''
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

# Create your tests here.
class QuestionModelTests(TestCase):
    '''Subclass with a method that creates a Question instance with a pub_date in the future'''

    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# Testing views
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    '''Subclass of django.test.TestCase for testing QuestionIndexView'''
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        Choice.objects.create(question=question, choice_text="Choice 1")
        Choice.objects.create(question=question, choice_text="Choice 2")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        future_question = create_question(question_text="Future question.", days=30)
        Choice.objects.create(question=question, choice_text="Choice")
        Choice.objects.create(question=future_question, choice_text="Choice Future")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        Choice.objects.create(question=question1, choice_text="Choice 1")
        Choice.objects.create(question=question2, choice_text="Choice 2")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

    def test_questions_with_no_choices_are_unpublished(self):
        """
        Questions with no choices are not published
        """
        create_question(question_text="Question with no choices.", days=-3)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_questions_with_choices_are_published(self):
        question = create_question(question_text="Question with choices.", days=-3)
        Choice.objects.create(question=question, choice_text="Choice 1")
        Choice.objects.create(question=question, choice_text="Choice 2")
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

class QuestionDetailViewTests(TestCase):
    '''Subclass of django.test.TestCase for testing QuestionDetailView'''
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        Choice.objects.create(question=past_question, choice_text="Choice One")
        Choice.objects.create(question=past_question, choice_text="Choice Two")
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    """Subclass of django.test.TestCase for testing ResultsView."""
    def test_future_results_view(self):
        """
        The results view of a question with a pub_date in the future
        returns a 404 not found error.
        """
        future_question = create_question(question_text="Future Question.", days=10)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_results_view(self):
        """
        The results view of a question with a pub_date in the past
        displays the question's results view
        """
        past_question = create_question(question_text="Past Question", days=-10)
        Choice.objects.create(question=past_question, choice_text="Choice One")
        Choice.objects.create(question=past_question, choice_text="Choice Two")
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
