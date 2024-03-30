from django.urls import path, include
from store import views
from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_settings/', views.UserSettingsView.as_view(), name='user_settings'),
]
