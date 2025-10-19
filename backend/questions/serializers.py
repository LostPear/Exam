from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    correctAnswer = serializers.IntegerField(source='correct_answer')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'type', 'difficulty', 'question', 'options', 'correctAnswer', 'explanation', 'image', 'createdAt']

class PublicQuestionSerializer(serializers.ModelSerializer):
    # Without exposing correct answer for exam creation if needed
    class Meta:
        model = Question
        fields = ['id', 'type', 'difficulty', 'question', 'options', 'image']
