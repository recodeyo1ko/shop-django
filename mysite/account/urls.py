from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registerUser/', views.register_user, name='register_user'),
    path('registerUserCommit/', views.register_user_commit, name='register_user_commit'),
    path('userInfo/', views.user_info, name='user_info'),
    path('updateUser/', views.update_user, name='update_user'),
    path('updateUserCommit/', views.update_user_commit, name='update_user_commit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]