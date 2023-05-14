from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('logIn/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('posts/', views.get_post, name='posts'),
    path('post-create/', views.create_post, name='create-post'),
    path('post-update/<id>', views.update_post, name='update-post'),
    path('post-delete/<id>', views.delete_post, name='delete-post'),
    path('comment-create/<pk>', views.create_comment, name='comment-create'),
    path('comment/', views.comment, name='comment'),
    path('logout/', views.logoutUser, name='logout'),
    path('posts-detail/<id>', views.post_detail, name='post-detail'),
    path('profile-edit/<id>', views.editProfile, name='profile-edit'),
    path('change-password/', views.PasswordsChangeView.as_view(), name='change-password'),
    path('success-password/', views.password_success, name='success-password'),
    path('users/', views.get_users, name='users'),
    path('users-update/<id>', views.update_users, name='users-update'),
    path('users-delete/<id>', views.delete_users, name='users-delete'),
    path('add-delete/', views.add_users, name='add-delete'),
    path('search/', views.search, name='search'),
    path('search-date/', views.search_date, name='search-date'),
    path('search-num/', views.search_num_visits, name='search-num'),
    path('post-able/', views.get_post_able, name='post-able'),
    path('history-posts/', views.get_post_history, name='history-posts'),
]
