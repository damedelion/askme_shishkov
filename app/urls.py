from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('tags/<str:tag>', views.tag, name='tag'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
]