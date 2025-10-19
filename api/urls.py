from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()

urlpatterns = [
    # 认证相关
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # 题目相关
    path('questions/', views.QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('questions/random/', views.RandomQuestionsView.as_view(), name='random-questions'),
    path('questions/sequential/', views.SequentialQuestionsView.as_view(), name='sequential-questions'),
    path('questions/import/', views.QuestionImportView.as_view(), name='question-import'),
    
    # 考试相关
    path('exams/', views.ExamListCreateView.as_view(), name='exam-list-create'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam-detail'),
    path('exams/<int:pk>/submit/', views.ExamSubmitView.as_view(), name='exam-submit'),
    path('exams/<int:pk>/result/', views.ExamResultView.as_view(), name='exam-result'),
    path('exams/history/', views.ExamHistoryView.as_view(), name='exam-history'),
    
    # 练习相关
    path('practice/', views.PracticeSessionListCreateView.as_view(), name='practice-list-create'),
    path('practice/<int:pk>/', views.PracticeSessionDetailView.as_view(), name='practice-detail'),
    
    # 用户管理（管理员）
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/stats/', views.UserStatsView.as_view(), name='user-stats'),
    path('users/stats/', views.UserStatsView.as_view(), name='my-stats'),
]