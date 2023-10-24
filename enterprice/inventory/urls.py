from django.urls import path

from .views import main_inventory

app_name = 'inventory'

urlpatterns = [
    path('', main_inventory, name='inventory')
]