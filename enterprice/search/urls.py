from django.urls import path
from .views import get_access

urlpatterns = [
    path('', get_access, name='login')
]
