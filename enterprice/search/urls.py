from django.contrib.auth import logout
from django.urls import path
from .views import get_access, update_load_document, search_engine, get_details_product, get_main_page, choice_projects, \
    user_logout, get_main_inventory, inventory_detail
from .utils.generate_context import clear_sort

urlpatterns = [
    path('', get_access, name='login'),
    path('main/', get_main_page, name='main'),
    path('update/', update_load_document, name='update'),
    path('find/', search_engine, name='find'),
    path('details/<int:id>', get_details_product, name='details'),
    path('choice/', choice_projects, name='choice'),
    path('clear/', clear_sort, name='clear'),
    path('logout/', user_logout, name='logout'),
    path('inventory/', get_main_inventory, name='inventory'),
    path('detail-product/<str:article>', inventory_detail, name='inventory_detail')



]
