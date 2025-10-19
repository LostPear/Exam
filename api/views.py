from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import UserProfile, Question, Exam, PracticeSession, QuestionImport
from .serializers import (
    UserSerializer, UserProfileSerializer, QuestionSerializer, QuestionCreateSerializer,
    ExamSerializer, ExamCreateSerializer, ExamSubmitSerializer, PracticeSessionSerializer,
    PracticeSessionCreateSerializer, QuestionImportSerializer, UserStatsSerializer,
    LoginSerializer, RegisterSerializer, ChangePasswordSerializer
)
import pandas as pd
import json
import os
from django.conf import settings


class RegisterView(APIView):
    """用户注册"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """用户登出"""
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """获取和更新用户资料"""
    
    def get(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # 更新用户基本信息
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        user.save()
        
        # 更新用户资料
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """修改密码"""
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': '密码修改成功'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionListCreateView(generics.ListCreateAPIView):
    """题目列表和创建"""
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer
    
    def get_queryset(self):
        queryset = Question.objects.all()
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(question__icontains=search) | 
                Q(explanation__icontains=search)
            )
        
        # 类型筛选
        question_type = self.request.query_params.get('type', None)
        if question_type:
            queryset = queryset.filter(type=question_type)
        
        # 难度筛选
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset.order_by('-created_at')


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """题目详情、更新和删除"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class RandomQuestionsView(APIView):
    """获取随机题目"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        count = int(request.query_params.get('count', 10))
        questions = Question.objects.all().order_by('?')[:count]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class SequentialQuestionsView(APIView):
    """获取顺序题目"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))
        questions = Question.objects.all().order_by('id')[offset:offset+limit]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionImportView(APIView):
    """题目导入"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': '没有上传文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        file_name = file.name
        
        # 保存文件
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file_name)
        
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # 创建导入记录
        import_record = QuestionImport.objects.create(
            user=request.user,
            file_name=file_name,
            file_path=file_path,
            status='processing'
        )
        
        try:
            # 处理文件
            self.process_import_file(file_path, import_record)
            import_record.status = 'completed'
            import_record.completed_at = timezone.now()
        except Exception as e:
            import_record.status = 'failed'
            import_record.error_messages.append(str(e))
        
        import_record.save()
        
        serializer = QuestionImportSerializer(import_record)
        return Response(serializer.data)
    
    def process_import_file(self, file_path, import_record):
        """处理导入文件"""
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        else:
            raise ValueError('不支持的文件格式')
        
        import_record.total_count = len(df)
        success_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # 解析题目数据
                question_data = {
                    'type': row.get('type', 'single'),
                    'difficulty': row.get('difficulty', 'medium'),
                    'question': str(row.get('question', '')),
                    'options': json.loads(row.get('options', '[]')) if isinstance(row.get('options'), str) else row.get('options', []),
                    'correct_answer': int(row.get('correct_answer', 0)),
                    'explanation': str(row.get('explanation', ''))
                }
                
                # 创建题目
                Question.objects.create(**question_data)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                import_record.error_messages.append(f"第{index+1}行: {str(e)}")
        
        import_record.success_count = success_count
        import_record.error_count = error_count


class ExamListCreateView(generics.ListCreateAPIView):
    """考试列表和创建"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExamCreateSerializer
        return ExamSerializer
    
    def get_queryset(self):
        return Exam.objects.filter(user=request.user).order_by('-created_at')


class ExamDetailView(generics.RetrieveAPIView):
    """考试详情"""
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Exam.objects.filter(user=self.request.user)


class ExamSubmitView(APIView):
    """提交考试"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk, user=request.user)
        except Exam.DoesNotExist:
            return Response({'error': '考试不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        if exam.submitted_at:
            return Response({'error': '考试已经提交'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExamSubmitSerializer(data=request.data)
        if serializer.is_valid():
            exam.answers = serializer.validated_data['answers']
            exam.calculate_score()
            exam.submitted_at = timezone.now()
            exam.save()
            
            return Response(ExamSerializer(exam).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamResultView(APIView):
    """获取考试结果"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk, user=request.user)
        except Exam.DoesNotExist:
            return Response({'error': '考试不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(ExamSerializer(exam).data)


class ExamHistoryView(APIView):
    """获取考试历史"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        exams = Exam.objects.filter(user=request.user).order_by('-created_at')
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)


class PracticeSessionListCreateView(generics.ListCreateAPIView):
    """练习会话列表和创建"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PracticeSessionCreateSerializer
        return PracticeSessionSerializer
    
    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user).order_by('-created_at')


class PracticeSessionDetailView(generics.RetrieveAPIView):
    """练习会话详情"""
    serializer_class = PracticeSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PracticeSession.objects.filter(user=self.request.user)


class UserListView(generics.ListAPIView):
    """用户列表（管理员）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只有管理员可以查看用户列表
        if not hasattr(self.request.user, 'profile') or self.request.user.profile.role != 'admin':
            return User.objects.none()
        return User.objects.all().order_by('-date_joined')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情（管理员）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只有管理员可以管理用户
        if not hasattr(self.request.user, 'profile') or self.request.user.profile.role != 'admin':
            return User.objects.none()
        return User.objects.all()


class UserStatsView(APIView):
    """用户统计信息"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk=None):
        if pk:
            # 管理员查看指定用户统计
            if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
                return Response({'error': '权限不足'}, status=status.HTTP_403_FORBIDDEN)
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 用户查看自己的统计
            user = request.user
        
        # 计算统计信息
        total_exams = Exam.objects.filter(user=user).count()
        passed_exams = Exam.objects.filter(user=user, passed=True).count()
        average_score = Exam.objects.filter(user=user, submitted_at__isnull=False).aggregate(
            avg_score=Avg('score')
        )['avg_score'] or 0
        
        total_practice_sessions = PracticeSession.objects.filter(user=user).count()
        
        # 计算答题统计
        from .models import PracticeQuestion
        practice_questions = PracticeQuestion.objects.filter(
            practice_session__user=user,
            answered=True
        )
        total_questions_answered = practice_questions.count()
        correct_answers = practice_questions.filter(is_correct=True).count()
        accuracy_rate = (correct_answers / total_questions_answered * 100) if total_questions_answered > 0 else 0
        
        stats = {
            'total_exams': total_exams,
            'passed_exams': passed_exams,
            'average_score': round(average_score, 2),
            'total_practice_sessions': total_practice_sessions,
            'total_questions_answered': total_questions_answered,
            'correct_answers': correct_answers,
            'accuracy_rate': round(accuracy_rate, 2)
        }
        
        return Response(stats)