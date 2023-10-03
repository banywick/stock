from django.urls import path
from .views import get_access, get_main_page, update_load_document

urlpatterns = [
    path('', get_access, name='login'),
    path('main/', get_main_page, name='main'),
    path('update/', update_load_document, name='update')
]
