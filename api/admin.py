from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Question, Exam, PracticeSession, QuestionImport


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('profile__role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else 'N/A'
    get_role.short_description = 'Role'


# 重新注册User模型
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'difficulty', 'question_short', 'correct_answer_text', 'created_at')
    list_filter = ('type', 'difficulty', 'created_at')
    search_fields = ('question', 'explanation')
    list_per_page = 20
    
    def question_short(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_short.short_description = 'Question'
    
    def correct_answer_text(self, obj):
        return obj.get_correct_answer_text()
    correct_answer_text.short_description = 'Correct Answer'


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_questions', 'correct_count', 'score', 'passed', 'created_at', 'submitted_at')
    list_filter = ('passed', 'created_at', 'submitted_at')
    search_fields = ('user__username', 'user__email')
    list_per_page = 20
    readonly_fields = ('created_at', 'submitted_at')


@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'practice_type', 'completed', 'created_at')
    list_filter = ('practice_type', 'completed', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_per_page = 20


@admin.register(QuestionImport)
class QuestionImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_name', 'status', 'total_count', 'success_count', 'error_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'file_name')
    list_per_page = 20
    readonly_fields = ('created_at', 'completed_at')