from typing import List, Dict
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from questions.models import Question
from questions.serializers import PublicQuestionSerializer
from .models import Exam

PASS_SCORE = 90
TOTAL_QUESTIONS = 100
SINGLE_COUNT = 90
JUDGE_COUNT = 10

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exam(request):
    # Select questions: 90 single + 10 judge (or as many as available)
    singles = list(Question.objects.filter(type='single').values_list('id', flat=True))
    judges = list(Question.objects.filter(type='judge').values_list('id', flat=True))
    from random import sample
    selected: List[int] = []
    if singles:
        selected += sample(singles, min(len(singles), SINGLE_COUNT))
    if judges:
        selected += sample(judges, min(len(judges), JUDGE_COUNT))
    # If not enough, fill from any type
    if len(selected) < TOTAL_QUESTIONS:
        others = list(Question.objects.exclude(id__in=selected).values_list('id', flat=True))
        if others:
            need = TOTAL_QUESTIONS - len(selected)
            selected += sample(others, min(len(others), need))
    # Build exam
    exam = Exam.objects.create(user=request.user, question_order=selected)
    if selected:
        exam.questions.add(*Question.objects.filter(id__in=selected))
    questions = Question.objects.filter(id__in=selected)
    # Keep order
    id_to_q = {q.id: q for q in questions}
    ordered = [id_to_q[qid] for qid in selected if qid in id_to_q]
    data = {
        'id': exam.id,
        'questions': PublicQuestionSerializer(ordered, many=True).data
    }
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id, user=request.user)
    questions = Question.objects.filter(id__in=exam.question_order)
    id_to_q = {q.id: q for q in questions}
    ordered = [id_to_q[qid] for qid in exam.question_order if qid in id_to_q]
    data = {
        'id': exam.id,
        'questions': PublicQuestionSerializer(ordered, many=True).data
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_exam(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id, user=request.user)
    answers: Dict[str, int] = request.data.get('answers', {}) or {}
    # Compute score
    questions = Question.objects.filter(id__in=exam.question_order)
    id_to_q = {q.id: q for q in questions}
    correct = 0
    wrong = 0
    unanswered = 0
    for index, qid in enumerate(exam.question_order):
        q = id_to_q.get(qid)
        user_ans = answers.get(str(index))
        if user_ans is None:
            unanswered += 1
        else:
            if q and int(user_ans) == q.correct_answer:
                correct += 1
            else:
                wrong += 1
    score = correct  # 1 point per question
    exam.answers = answers
    exam.score = score
    exam.passed = score >= PASS_SCORE
    exam.submitted_at = timezone.now()
    exam.save()
    return Response({'message': '提交成功', 'score': score, 'passed': exam.passed})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_result(request, exam_id: int):
    exam = get_object_or_404(Exam, id=exam_id, user=request.user)
    questions = Question.objects.filter(id__in=exam.question_order)
    id_to_q = {q.id: q for q in questions}
    correct = 0
    wrong = 0
    unanswered = 0
    wrong_questions = []
    for index, qid in enumerate(exam.question_order):
        q = id_to_q.get(qid)
        user_ans = exam.answers.get(str(index)) if isinstance(exam.answers, dict) else None
        if user_ans is None:
            unanswered += 1
        elif q and int(user_ans) == q.correct_answer:
            correct += 1
        else:
            wrong += 1
            if q:
                wrong_questions.append({
                    'id': q.id,
                    'number': index + 1,
                    'type': q.type,
                    'question': q.question,
                    'options': q.options,
                    'correctAnswer': q.correct_answer,
                    'userAnswer': int(user_ans) if user_ans is not None else None,
                    'explanation': q.explanation,
                })
    score = exam.score if exam.score is not None else correct
    duration_seconds = 0
    if exam.submitted_at:
        duration_seconds = int((exam.submitted_at - exam.created_at).total_seconds())
    minutes = duration_seconds // 60
    duration_text = f"{minutes}分钟" if minutes > 0 else "不足1分钟"
    total = len(exam.question_order)
    accuracy = int((correct / total) * 100) if total else 0
    data = {
        'score': score,
        'correct': correct,
        'wrong': wrong,
        'unanswered': unanswered,
        'passed': exam.passed,
        'duration': duration_text,
        'accuracy': accuracy,
        'wrongQuestions': wrong_questions,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_history(request):
    exams = Exam.objects.filter(user=request.user).order_by('-created_at')[:50]
    results = []
    for e in exams:
        total = len(e.question_order)
        correct = e.score if e.score is not None else 0
        minutes = 0
        if e.submitted_at:
            minutes = int((e.submitted_at - e.created_at).total_seconds() // 60)
        results.append({
            'id': e.id,
            'title': '科目一模拟考试',
            'date': e.created_at.strftime('%Y-%m-%d'),
            'duration': f'{minutes}分钟' if minutes else '—',
            'score': correct,
            'correct': correct,
            'total': total,
            'passed': bool(e.passed),
        })
    return Response({'results': results})
