from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history_view, name='history'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
]