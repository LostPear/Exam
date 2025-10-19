"""
序列化器定义
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Question, Exam, ExamQuestion, PracticeRecord, UserStats


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码不一致"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # 创建用户统计记录
        UserStats.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'avatar', 'phone', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户账号已被禁用')
        else:
            raise serializers.ValidationError('必须提供用户名和密码')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码不正确')
        return value


class UpdateProfileSerializer(serializers.ModelSerializer):
    """更新个人资料序列化器"""
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar')


class QuestionSerializer(serializers.ModelSerializer):
    """题目序列化器"""
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_options(self, value):
        """验证选项格式"""
        if not isinstance(value, list):
            raise serializers.ValidationError('选项必须是数组格式')
        if len(value) < 2:
            raise serializers.ValidationError('选项至少需要2个')
        return value

    def validate(self, attrs):
        """验证正确答案索引"""
        if 'correct_answer' in attrs and 'options' in attrs:
            if attrs['correct_answer'] >= len(attrs['options']):
                raise serializers.ValidationError('正确答案索引超出选项范围')
        return attrs


class QuestionListSerializer(serializers.ModelSerializer):
    """题目列表序列化器（简化版）"""
    class Meta:
        model = Question
        fields = ('id', 'type', 'difficulty', 'question', 'category', 'created_at')


class ExamQuestionSerializer(serializers.ModelSerializer):
    """考试题目序列化器"""
    question_detail = QuestionSerializer(source='question', read_only=True)
    
    class Meta:
        model = ExamQuestion
        fields = ('id', 'question', 'question_detail', 'user_answer', 'is_correct', 'order')


class ExamSerializer(serializers.ModelSerializer):
    """考试序列化器"""
    exam_questions = ExamQuestionSerializer(many=True, read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ('user', 'score', 'passed', 'correct_count', 'wrong_count', 
                           'submitted_at', 'created_at')


class ExamCreateSerializer(serializers.Serializer):
    """创建考试序列化器"""
    question_count = serializers.IntegerField(min_value=1, max_value=100, default=50)
    difficulty = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard', 'all'],
        default='all',
        required=False
    )


class ExamSubmitSerializer(serializers.Serializer):
    """提交考试序列化器"""
    answers = serializers.DictField(
        child=serializers.IntegerField(),
        help_text='题目ID和答案的映射，例如: {"1": 0, "2": 1, "3": 2}'
    )


class ExamResultSerializer(serializers.ModelSerializer):
    """考试结果序列化器"""
    exam_questions = ExamQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = ('id', 'status', 'score', 'passed', 'total_questions', 
                 'correct_count', 'wrong_count', 'duration', 'created_at', 
                 'submitted_at', 'exam_questions')


class PracticeRecordSerializer(serializers.ModelSerializer):
    """练习记录序列化器"""
    question_detail = QuestionSerializer(source='question', read_only=True)
    
    class Meta:
        model = PracticeRecord
        fields = '__all__'
        read_only_fields = ('user', 'is_correct', 'created_at')

    def create(self, validated_data):
        # 自动判断答案是否正确
        question = validated_data['question']
        user_answer = validated_data['user_answer']
        validated_data['is_correct'] = (user_answer == question.correct_answer)
        
        # 更新用户统计
        user = validated_data['user']
        stats, created = UserStats.objects.get_or_create(user=user)
        stats.total_practice += 1
        if validated_data['is_correct']:
            stats.correct_practice += 1
        stats.last_practice_at = timezone.now()
        stats.save()
        
        return super().create(validated_data)


class UserStatsSerializer(serializers.ModelSerializer):
    """用户统计序列化器"""
    practice_accuracy = serializers.ReadOnlyField()
    exam_pass_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = UserStats
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器（含统计数据）"""
    stats = UserStatsSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'avatar', 'phone', 
                 'created_at', 'updated_at', 'stats')
        read_only_fields = ('id', 'created_at', 'updated_at')


class QuestionImportSerializer(serializers.Serializer):
    """题目导入序列化器"""
    file = serializers.FileField(required=True)
    
    def validate_file(self, value):
        """验证文件格式"""
        ext = value.name.split('.')[-1].lower()
        if ext not in ['xlsx', 'xls', 'csv', 'json']:
            raise serializers.ValidationError('仅支持 Excel、CSV 和 JSON 格式')
        return value
