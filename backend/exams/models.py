from django.db import models
from django.contrib.auth.models import User
from questions.models import Question

class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    questions = models.ManyToManyField(Question, related_name='exams', blank=True)
    question_order = models.JSONField(default=list)  # list of question ids in order
    answers = models.JSONField(default=dict, blank=True)  # index -> selected option index
    score = models.IntegerField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def total_questions(self) -> int:
        return len(self.question_order)
