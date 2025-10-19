"""
视图定义
"""
import json
import pandas as pd
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Question, Exam, ExamQuestion, PracticeRecord, UserStats
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    ChangePasswordSerializer, UpdateProfileSerializer, UserDetailSerializer,
    QuestionSerializer, QuestionListSerializer, QuestionImportSerializer,
    ExamSerializer, ExamCreateSerializer, ExamSubmitSerializer, ExamResultSerializer,
    PracticeRecordSerializer, UserStatsSerializer
)
from .permissions import IsAdminUser


# 认证相关视图
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """用户注册"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """用户登出"""
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"message": "登出成功"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """获取/更新个人资料"""
    user = request.user
    
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserDetailSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """修改密码"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "密码修改成功"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 题目相关视图
class QuestionViewSet(viewsets.ModelViewSet):
    """题目管理视图集"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionListSerializer
        return QuestionSerializer
    
    def get_permissions(self):
        """根据操作设置权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """支持搜索和筛选"""
        queryset = Question.objects.all()
        
        # 搜索
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(question__icontains=search) | 
                Q(category__icontains=search)
            )
        
        # 按类型筛选
        question_type = self.request.query_params.get('type', None)
        if question_type:
            queryset = queryset.filter(type=question_type)
        
        # 按难度筛选
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # 按分类筛选
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def random(self, request):
        """获取随机题目"""
        count = int(request.query_params.get('count', 1))
        difficulty = request.query_params.get('difficulty', None)
        
        queryset = Question.objects.all()
        if difficulty and difficulty != 'all':
            queryset = queryset.filter(difficulty=difficulty)
        
        questions = queryset.order_by('?')[:count]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sequential(self, request):
        """获取顺序题目"""
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 1))
        
        questions = Question.objects.all()[offset:offset+limit]
        serializer = QuestionSerializer(questions, many=True)
        return Response({
            'questions': serializer.data,
            'total': Question.objects.count(),
            'offset': offset,
            'limit': limit,
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def import_questions(self, request):
        """批量导入题目"""
        serializer = QuestionImportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']
        file_ext = file.name.split('.')[-1].lower()
        
        try:
            questions_data = []
            
            if file_ext in ['xlsx', 'xls']:
                # 读取Excel文件
                df = pd.read_excel(file)
                questions_data = df.to_dict('records')
            
            elif file_ext == 'csv':
                # 读取CSV文件
                df = pd.read_csv(file)
                questions_data = df.to_dict('records')
            
            elif file_ext == 'json':
                # 读取JSON文件
                questions_data = json.load(file)
            
            # 批量创建题目
            created_count = 0
            errors = []
            
            for idx, data in enumerate(questions_data):
                try:
                    # 处理options字段
                    if isinstance(data.get('options'), str):
                        data['options'] = json.loads(data['options'])
                    
                    question_serializer = QuestionSerializer(data=data)
                    if question_serializer.is_valid():
                        question_serializer.save()
                        created_count += 1
                    else:
                        errors.append(f"第{idx+1}行: {question_serializer.errors}")
                except Exception as e:
                    errors.append(f"第{idx+1}行: {str(e)}")
            
            return Response({
                'message': f'成功导入 {created_count} 道题目',
                'created_count': created_count,
                'total_count': len(questions_data),
                'errors': errors
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'error': f'文件解析失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


# 考试相关视图
class ExamViewSet(viewsets.ModelViewSet):
    """考试管理视图集"""
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """只返回当前用户的考试"""
        user = self.request.user
        if user.role == 'admin':
            return Exam.objects.all()
        return Exam.objects.filter(user=user)
    
    def create(self, request):
        """创建新考试"""
        serializer = ExamCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        question_count = serializer.validated_data['question_count']
        difficulty = serializer.validated_data.get('difficulty', 'all')
        
        # 筛选题目
        questions_query = Question.objects.all()
        if difficulty and difficulty != 'all':
            questions_query = questions_query.filter(difficulty=difficulty)
        
        # 随机抽取题目
        questions = questions_query.order_by('?')[:question_count]
        
        if len(questions) < question_count:
            return Response({
                'error': f'题库中符合条件的题目不足，仅有 {len(questions)} 道题'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建考试
        exam = Exam.objects.create(
            user=request.user,
            total_questions=len(questions)
        )
        
        # 创建考试题目关联
        for idx, question in enumerate(questions):
            ExamQuestion.objects.create(
                exam=exam,
                question=question,
                order=idx
            )
        
        exam_serializer = ExamSerializer(exam)
        return Response(exam_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """提交考试"""
        exam = self.get_object()
        
        if exam.status == 'completed':
            return Response({'error': '考试已提交'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExamSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        answers = serializer.validated_data['answers']
        
        # 批量更新答案并判断正确性
        correct_count = 0
        wrong_count = 0
        
        exam_questions = exam.exam_questions.all()
        for eq in exam_questions:
            question_id = str(eq.question.id)
            if question_id in answers:
                user_answer = answers[question_id]
                eq.user_answer = user_answer
                eq.is_correct = (user_answer == eq.question.correct_answer)
                eq.save()
                
                if eq.is_correct:
                    correct_count += 1
                else:
                    wrong_count += 1
        
        # 计算分数（每题2分，满分100分）
        score = int((correct_count / exam.total_questions) * 100)
        passed = score >= 90  # 90分及格
        
        # 计算考试时长（秒）
        duration = int((timezone.now() - exam.created_at).total_seconds())
        
        # 更新考试状态
        exam.status = 'completed'
        exam.score = score
        exam.passed = passed
        exam.correct_count = correct_count
        exam.wrong_count = wrong_count
        exam.duration = duration
        exam.submitted_at = timezone.now()
        exam.save()
        
        # 更新用户统计
        stats, created = UserStats.objects.get_or_create(user=request.user)
        stats.total_exams += 1
        if passed:
            stats.passed_exams += 1
        stats.save()
        
        return Response({
            'message': '考试提交成功',
            'score': score,
            'passed': passed,
            'correct_count': correct_count,
            'wrong_count': wrong_count,
        })
    
    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        """获取考试结果"""
        exam = self.get_object()
        
        if exam.status != 'completed':
            return Response({'error': '考试尚未完成'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExamResultSerializer(exam)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """获取考试历史"""
        exams = self.get_queryset().filter(status='completed')
        
        # 支持分页
        page = self.paginate_queryset(exams)
        if page is not None:
            serializer = ExamSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)


# 练习记录相关视图
class PracticeRecordViewSet(viewsets.ModelViewSet):
    """练习记录视图集"""
    queryset = PracticeRecord.objects.all()
    serializer_class = PracticeRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """只返回当前用户的练习记录"""
        return PracticeRecord.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """创建练习记录时自动设置用户"""
        serializer.save(user=self.request.user)


# 用户管理相关视图
class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        """支持搜索"""
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """获取用户统计信息"""
        user = self.get_object()
        stats, created = UserStats.objects.get_or_create(user=user)
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)


# 统计相关视图
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats_view(request):
    """获取当前用户统计信息"""
    stats, created = UserStats.objects.get_or_create(user=request.user)
    serializer = UserStatsSerializer(stats)
    return Response(serializer.data)
