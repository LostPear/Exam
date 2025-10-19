from django.urls import path
from .views import list_users, retrieve_user, update_user, delete_user, user_stats

urlpatterns = [
    path('', list_users, name='users-list'),
    path('<int:user_id>/', retrieve_user, name='users-detail'),
    path('<int:user_id>/stats/', user_stats, name='users-stats'),
    path('<int:user_id>/', update_user, name='users-update'),
    path('<int:user_id>/', delete_user, name='users-delete'),
]
