from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=[
        ('user', '普通用户'),
        ('admin', '管理员')
    ], default='user')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Question(models.Model):
    """题目模型"""
    TYPE_CHOICES = [
        ('single', '单选题'),
        ('judge', '判断题'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='题目类型')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name='难度')
    question = models.TextField(verbose_name='题目内容')
    options = models.JSONField(verbose_name='选项', help_text='存储选项数组，如["A.选项1", "B.选项2", "C.选项3", "D.选项4"]')
    correct_answer = models.IntegerField(verbose_name='正确答案索引', help_text='0表示A，1表示B，以此类推')
    explanation = models.TextField(verbose_name='解析', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.question[:50]}..."
    
    def get_correct_answer_text(self):
        """获取正确答案的文本"""
        if self.type == 'judge':
            return '正确' if self.correct_answer == 0 else '错误'
        else:
            return self.options[self.correct_answer] if self.options else ''


class Exam(models.Model):
    """考试模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    questions = models.ManyToManyField(Question, through='ExamQuestion')
    answers = models.JSONField(default=dict, verbose_name='用户答案', help_text='存储用户答案，格式：{question_id: answer_index}')
    score = models.IntegerField(null=True, blank=True, verbose_name='得分')
    total_questions = models.IntegerField(default=0, verbose_name='总题数')
    correct_count = models.IntegerField(default=0, verbose_name='正确题数')
    passed = models.BooleanField(default=False, verbose_name='是否通过')
    time_limit = models.IntegerField(default=45, verbose_name='时间限制(分钟)')
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = '考试'
        verbose_name_plural = '考试'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - 考试 {self.id}"
    
    def calculate_score(self):
        """计算得分"""
        if not self.answers:
            return 0
        
        correct_count = 0
        for question_id, answer in self.answers.items():
            try:
                question = Question.objects.get(id=question_id)
                if answer == question.correct_answer:
                    correct_count += 1
            except Question.DoesNotExist:
                continue
        
        self.correct_count = correct_count
        self.total_questions = self.questions.count()
        self.score = int((correct_count / self.total_questions * 100)) if self.total_questions > 0 else 0
        self.passed = self.score >= 90  # 90分及格
        return self.score


class ExamQuestion(models.Model):
    """考试题目关联模型"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name='题目顺序')
    
    class Meta:
        verbose_name = '考试题目'
        verbose_name_plural = '考试题目'
        unique_together = ['exam', 'question']
        ordering = ['order']


class PracticeSession(models.Model):
    """练习会话模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    questions = models.ManyToManyField(Question, through='PracticeQuestion')
    practice_type = models.CharField(max_length=20, choices=[
        ('sequential', '顺序练习'),
        ('random', '随机练习'),
    ], verbose_name='练习类型')
    answers = models.JSONField(default=dict, verbose_name='用户答案')
    current_question_index = models.IntegerField(default=0, verbose_name='当前题目索引')
    completed = models.BooleanField(default=False, verbose_name='是否完成')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '练习会话'
        verbose_name_plural = '练习会话'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_practice_type_display()}"


class PracticeQuestion(models.Model):
    """练习题目关联模型"""
    practice_session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name='题目顺序')
    answered = models.BooleanField(default=False, verbose_name='是否已答')
    user_answer = models.IntegerField(null=True, blank=True, verbose_name='用户答案')
    is_correct = models.BooleanField(null=True, blank=True, verbose_name='是否正确')
    
    class Meta:
        verbose_name = '练习题目'
        verbose_name_plural = '练习题目'
        unique_together = ['practice_session', 'question']
        ordering = ['order']


class QuestionImport(models.Model):
    """题目导入记录模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '完成'),
        ('failed', '失败'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_imports')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_path = models.CharField(max_length=500, verbose_name='文件路径')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    total_count = models.IntegerField(default=0, verbose_name='总数量')
    success_count = models.IntegerField(default=0, verbose_name='成功数量')
    error_count = models.IntegerField(default=0, verbose_name='失败数量')
    error_messages = models.JSONField(default=list, verbose_name='错误信息')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = '题目导入'
        verbose_name_plural = '题目导入'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file_name} - {self.get_status_display()}"