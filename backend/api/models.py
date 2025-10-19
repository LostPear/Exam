"""
数据模型定义
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """扩展用户模型"""
    ROLE_CHOICES = [
        ('user', '普通用户'),
        ('admin', '管理员'),
    ]
    
    email = models.EmailField('邮箱', unique=True)
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username


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
    
    type = models.CharField('题目类型', max_length=10, choices=TYPE_CHOICES)
    difficulty = models.CharField('难度', max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    question = models.TextField('题目内容')
    options = models.JSONField('选项', help_text='选项数组，例如: ["选项A", "选项B", "选项C", "选项D"]')
    correct_answer = models.IntegerField('正确答案', help_text='正确答案的索引，从0开始')
    explanation = models.TextField('答案解析', blank=True, default='')
    image = models.ImageField('题目图片', upload_to='questions/', null=True, blank=True)
    category = models.CharField('题目分类', max_length=50, blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.question[:50]}"


class Exam(models.Model):
    """考试模型"""
    STATUS_CHOICES = [
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams', verbose_name='考生')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.IntegerField('分数', null=True, blank=True)
    passed = models.BooleanField('是否通过', default=False)
    total_questions = models.IntegerField('题目总数', default=0)
    correct_count = models.IntegerField('正确数量', default=0)
    wrong_count = models.IntegerField('错误数量', default=0)
    duration = models.IntegerField('考试时长（秒）', null=True, blank=True, help_text='用户实际花费的时间')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    submitted_at = models.DateTimeField('提交时间', null=True, blank=True)
    
    class Meta:
        verbose_name = '考试'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ExamQuestion(models.Model):
    """考试题目关联模型"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_questions', verbose_name='考试')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='题目')
    user_answer = models.IntegerField('用户答案', null=True, blank=True, help_text='用户选择的答案索引')
    is_correct = models.BooleanField('是否正确', null=True, blank=True)
    order = models.IntegerField('题目顺序', default=0)
    
    class Meta:
        verbose_name = '考试题目'
        verbose_name_plural = verbose_name
        ordering = ['order']
        unique_together = ['exam', 'question']
    
    def __str__(self):
        return f"{self.exam} - {self.question}"


class PracticeRecord(models.Model):
    """练习记录模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_records', verbose_name='用户')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='题目')
    user_answer = models.IntegerField('用户答案', help_text='用户选择的答案索引')
    is_correct = models.BooleanField('是否正确')
    practice_type = models.CharField('练习类型', max_length=20, choices=[
        ('sequential', '顺序练习'),
        ('random', '随机练习'),
    ])
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '练习记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.question}"


class UserStats(models.Model):
    """用户统计模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats', verbose_name='用户')
    total_exams = models.IntegerField('考试总数', default=0)
    passed_exams = models.IntegerField('通过考试数', default=0)
    total_practice = models.IntegerField('练习总数', default=0)
    correct_practice = models.IntegerField('练习正确数', default=0)
    study_time = models.IntegerField('学习时长（分钟）', default=0)
    last_practice_at = models.DateTimeField('最后练习时间', null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '用户统计'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.user.username} - 统计数据"
    
    @property
    def practice_accuracy(self):
        """练习正确率"""
        if self.total_practice == 0:
            return 0
        return round(self.correct_practice / self.total_practice * 100, 2)
    
    @property
    def exam_pass_rate(self):
        """考试通过率"""
        if self.total_exams == 0:
            return 0
        return round(self.passed_exams / self.total_exams * 100, 2)
