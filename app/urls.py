from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('tags/<str:tag>', views.tag, name='tag'),
    path('signup', views.sign_up, name='signup'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('<int:question_id>/like_question', views.like_question, name='like_question'),
    path('<int:answer_id>/answer_like', views.like_answer, name='like_answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)