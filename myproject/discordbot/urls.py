from django.urls import path
from . import views

urlpatterns = [
    path('generate-bot/', views.GenerateBotView.as_view(), name='generate_bot'),
    path('llm/', views.llm_api),
]