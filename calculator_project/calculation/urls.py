from django.urls import path
from . import views


urlpatterns = [
    path('evaluate/', views.evaluate, name='evaluate_expression'),
    path('history/', views.history, name='calculation_history'),
]