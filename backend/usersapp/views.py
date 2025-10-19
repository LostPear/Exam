from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from exams.models import Exam
from .serializers import AdminUserSerializer, AdminUserUpdateSerializer

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all().order_by('id')
    # Simple pagination using query params
    page = int(request.query_params.get('page', '1'))
    page_size = int(request.query_params.get('page_size', '10'))
    start = (page - 1) * page_size
    end = start + page_size
    data = AdminUserSerializer(users[start:end], many=True).data
    return Response({'results': data, 'count': users.count()})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def retrieve_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return Response(AdminUserSerializer(user).data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message': '更新成功'})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_stats(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    exams = Exam.objects.filter(user=user, submitted_at__isnull=False)
    practice_count = sum(len(e.answers) for e in exams if isinstance(e.answers, dict))
    exam_count = exams.count()
    total_correct = sum(e.score or 0 for e in exams)
    total_questions = sum(len(e.question_order) for e in exams)
    accuracy = int((total_correct / total_questions) * 100) if total_questions else 0
    return Response({
        'practiceCount': practice_count,
        'examCount': exam_count,
        'accuracy': accuracy,
    })
