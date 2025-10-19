from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, Question, Exam, ExamQuestion, PracticeSession, PracticeQuestion, QuestionImport


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    role = serializers.CharField(source='profile.role', read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    """题目序列化器"""
    correct_answer_text = serializers.CharField(source='get_correct_answer_text', read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'type', 'difficulty', 'question', 'options', 'correct_answer', 'correct_answer_text', 'explanation', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """题目创建序列化器"""
    
    class Meta:
        model = Question
        fields = ['type', 'difficulty', 'question', 'options', 'correct_answer', 'explanation']
    
    def validate_options(self, value):
        """验证选项格式"""
        if not isinstance(value, list) or len(value) < 2:
            raise serializers.ValidationError("选项必须是一个包含至少2个元素的数组")
        return value
    
    def validate_correct_answer(self, value):
        """验证正确答案索引"""
        options = self.initial_data.get('options', [])
        if value < 0 or value >= len(options):
            raise serializers.ValidationError("正确答案索引超出范围")
        return value


class ExamQuestionSerializer(serializers.ModelSerializer):
    """考试题目序列化器"""
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = ExamQuestion
        fields = ['id', 'question', 'order']


class ExamSerializer(serializers.ModelSerializer):
    """考试序列化器"""
    questions = ExamQuestionSerializer(source='examquestion_set', many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'user', 'questions', 'answers', 'score', 'total_questions', 'correct_count', 'passed', 'time_limit', 'created_at', 'submitted_at']
        read_only_fields = ['id', 'user', 'score', 'total_questions', 'correct_count', 'passed', 'created_at', 'submitted_at']


class ExamCreateSerializer(serializers.ModelSerializer):
    """考试创建序列化器"""
    
    class Meta:
        model = Exam
        fields = ['time_limit']
    
    def create(self, validated_data):
        user = self.context['request'].user
        exam = Exam.objects.create(user=user, **validated_data)
        
        # 随机选择题目
        questions = Question.objects.all().order_by('?')[:50]  # 默认50题
        for i, question in enumerate(questions):
            ExamQuestion.objects.create(exam=exam, question=question, order=i)
        
        exam.total_questions = questions.count()
        exam.save()
        return exam


class ExamSubmitSerializer(serializers.Serializer):
    """考试提交序列化器"""
    answers = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="用户答案，格式：{question_id: answer_index}"
    )
    
    def validate_answers(self, value):
        """验证答案格式"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("答案必须是字典格式")
        return value


class PracticeQuestionSerializer(serializers.ModelSerializer):
    """练习题目序列化器"""
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = PracticeQuestion
        fields = ['id', 'question', 'order', 'answered', 'user_answer', 'is_correct']


class PracticeSessionSerializer(serializers.ModelSerializer):
    """练习会话序列化器"""
    questions = PracticeQuestionSerializer(source='practicequestion_set', many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PracticeSession
        fields = ['id', 'user', 'questions', 'practice_type', 'answers', 'current_question_index', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'completed', 'created_at', 'updated_at']


class PracticeSessionCreateSerializer(serializers.ModelSerializer):
    """练习会话创建序列化器"""
    
    class Meta:
        model = PracticeSession
        fields = ['practice_type']
    
    def create(self, validated_data):
        user = self.context['request'].user
        practice_type = validated_data['practice_type']
        
        # 根据练习类型选择题目
        if practice_type == 'sequential':
            questions = Question.objects.all().order_by('id')
        else:  # random
            questions = Question.objects.all().order_by('?')
        
        # 限制练习题目数量
        questions = questions[:20]  # 默认20题
        
        practice_session = PracticeSession.objects.create(
            user=user,
            practice_type=practice_type
        )
        
        for i, question in enumerate(questions):
            PracticeQuestion.objects.create(
                practice_session=practice_session,
                question=question,
                order=i
            )
        
        return practice_session


class QuestionImportSerializer(serializers.ModelSerializer):
    """题目导入序列化器"""
    
    class Meta:
        model = QuestionImport
        fields = ['id', 'file_name', 'status', 'total_count', 'success_count', 'error_count', 'error_messages', 'created_at', 'completed_at']
        read_only_fields = ['id', 'status', 'total_count', 'success_count', 'error_count', 'error_messages', 'created_at', 'completed_at']


class UserStatsSerializer(serializers.Serializer):
    """用户统计序列化器"""
    total_exams = serializers.IntegerField()
    passed_exams = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_practice_sessions = serializers.IntegerField()
    total_questions_answered = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    accuracy_rate = serializers.FloatField()


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户账户已被禁用')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('用户名和密码不能为空')
        
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # 创建用户资料
        UserProfile.objects.create(user=user, role='user')
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('两次输入的新密码不一致')
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value