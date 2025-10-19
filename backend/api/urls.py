"""
API URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_view, login_view, logout_view, profile_view, change_password_view,
    QuestionViewSet, ExamViewSet, PracticeRecordViewSet, UserViewSet,
    user_stats_view
)

# 创建路由器
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'practice', PracticeRecordViewSet, basename='practice')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # 认证相关
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/profile/', profile_view, name='profile'),
    path('auth/change-password/', change_password_view, name='change-password'),
    
    # 统计相关
    path('stats/', user_stats_view, name='user-stats'),
    
    # 路由器注册的URL
    path('', include(router.urls)),
]
