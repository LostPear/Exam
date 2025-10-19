from django.urls import path
from .views import create_exam, get_exam, submit_exam, get_exam_result, get_exam_history

urlpatterns = [
    path('', create_exam, name='create-exam'),
    path('<int:exam_id>/', get_exam, name='get-exam'),
    path('<int:exam_id>/submit/', submit_exam, name='submit-exam'),
    path('<int:exam_id>/result/', get_exam_result, name='exam-result'),
    path('history/', get_exam_history, name='exam-history'),
]
