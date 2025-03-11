from django.urls import path
from . import views

urlpatterns = [
    path('api/generate-bot/', views.GenerateBotView.as_view(), name='generate_bot'),
]