import csv
import io
import json
from typing import List
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Question
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'import_questions']:
            return [IsAdminUser()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search')
        qtype = request.query_params.get('type')
        difficulty = request.query_params.get('difficulty')
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(Q(question__icontains=search) | Q(explanation__icontains=search))
        if qtype:
            queryset = queryset.filter(type=qtype)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})

    @action(detail=False, methods=['get'], url_path='random')
    def random_questions(self, request):
        try:
            count = int(request.query_params.get('count', '20'))
        except ValueError:
            count = 20
        ids = list(Question.objects.values_list('id', flat=True))
        if not ids:
            return Response({'results': []})
        from random import sample
        selected_ids = sample(ids, k=min(count, len(ids)))
        selected = Question.objects.filter(id__in=selected_ids)
        # Preserve input order
        id_to_q = {q.id: q for q in selected}
        ordered = [id_to_q[i] for i in selected_ids if i in id_to_q]
        data = QuestionSerializer(ordered, many=True).data
        return Response({'results': data})

    @action(detail=False, methods=['get'], url_path='sequential')
    def sequential_questions(self, request):
        try:
            limit = int(request.query_params.get('limit', '50'))
        except ValueError:
            limit = 50
        queryset = Question.objects.all()[: max(0, limit)]
        data = QuestionSerializer(queryset, many=True).data
        return Response({'results': data})

    @action(detail=False, methods=['post'], url_path='import')
    def import_questions(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'message': '未提供文件'}, status=status.HTTP_400_BAD_REQUEST)
        content_type = file.content_type or ''
        filename = getattr(file, 'name', '')
        success = 0
        failed = 0
        try:
            if content_type == 'application/json' or filename.endswith('.json'):
                payload = json.load(file)
                items: List[dict]
                if isinstance(payload, dict) and 'questions' in payload:
                    items = payload['questions']
                elif isinstance(payload, list):
                    items = payload
                else:
                    return Response({'message': 'JSON 格式不正确'}, status=status.HTTP_400_BAD_REQUEST)
                for item in items:
                    try:
                        Question.objects.create(
                            type=item.get('type', 'single'),
                            difficulty=item.get('difficulty', 'easy'),
                            question=item['question'],
                            options=item.get('options', []),
                            correct_answer=item.get('correctAnswer', 0),
                            explanation=item.get('explanation', ''),
                        )
                        success += 1
                    except Exception:
                        failed += 1
            elif 'csv' in content_type or filename.endswith('.csv'):
                data = file.read().decode('utf-8')
                reader = csv.DictReader(io.StringIO(data))
                for row in reader:
                    try:
                        options = [row.get('选项A') or row.get('A') or '', row.get('选项B') or row.get('B') or '']
                        # Optional C/D
                        if row.get('选项C') or row.get('C'):
                            options.append(row.get('选项C') or row.get('C'))
                        if row.get('选项D') or row.get('D'):
                            options.append(row.get('选项D') or row.get('D'))
                        correct = row.get('正确答案') or row.get('correctAnswer') or '0'
                        Question.objects.create(
                            type=row.get('题目类型') or row.get('type') or 'single',
                            difficulty=row.get('难度') or row.get('difficulty') or 'easy',
                            question=row.get('题目内容') or row.get('question') or '',
                            options=options,
                            correct_answer=int(correct) if str(correct).isdigit() else 0,
                            explanation=row.get('答案解析') or row.get('explanation') or '',
                        )
                        success += 1
                    except Exception:
                        failed += 1
            else:
                return Response({'message': '仅支持 JSON 或 CSV 导入'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'导入失败: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '导入完成', 'stats': {'success': success, 'failed': failed}})
