from site import venv
from django.urls import path
from . import views

urlpatterns = [
    path('v1/foods/', views.get_foods)
]