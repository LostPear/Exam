"""
Django Admin配置
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Question, Exam, ExamQuestion, PracticeRecord, UserStats


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('role', 'phone', 'avatar')}),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """题目管理"""
    list_display = ('id', 'type', 'difficulty', 'question_preview', 'category', 'created_at')
    list_filter = ('type', 'difficulty', 'category')
    search_fields = ('question', 'category')
    ordering = ('-created_at',)
    
    def question_preview(self, obj):
        """题目预览"""
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = '题目内容'


class ExamQuestionInline(admin.TabularInline):
    """考试题目内联"""
    model = ExamQuestion
    extra = 0
    readonly_fields = ('question', 'user_answer', 'is_correct')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """考试管理"""
    list_display = ('id', 'user', 'status', 'score', 'passed', 'created_at', 'submitted_at')
    list_filter = ('status', 'passed')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    inlines = [ExamQuestionInline]
    readonly_fields = ('user', 'score', 'passed', 'created_at', 'submitted_at')


@admin.register(PracticeRecord)
class PracticeRecordAdmin(admin.ModelAdmin):
    """练习记录管理"""
    list_display = ('id', 'user', 'question_preview', 'is_correct', 'practice_type', 'created_at')
    list_filter = ('is_correct', 'practice_type')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('user', 'question', 'user_answer', 'is_correct', 'created_at')
    
    def question_preview(self, obj):
        """题目预览"""
        return obj.question.question[:30] + '...' if len(obj.question.question) > 30 else obj.question.question
    question_preview.short_description = '题目'


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    """用户统计管理"""
    list_display = ('user', 'total_exams', 'passed_exams', 'total_practice', 
                   'practice_accuracy', 'exam_pass_rate', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'practice_accuracy', 'exam_pass_rate')
