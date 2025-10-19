from rest_framework import serializers
from questions.serializers import QuestionSerializer, PublicQuestionSerializer
from .models import Exam

class ExamCreateResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    questions = PublicQuestionSerializer(many=True)

class ExamDetailSerializer(serializers.ModelSerializer):
    questions = PublicQuestionSerializer(many=True, read_only=True, source='get_questions')

    class Meta:
        model = Exam
        fields = ['id', 'questions', 'created_at']

