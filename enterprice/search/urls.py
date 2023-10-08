from django.urls import path
from .views import get_access, get_main_page, update_load_document, search_engine, get_details_product

urlpatterns = [
    path('', get_access, name='login'),
    path('main/', get_main_page, name='main'),
    path('update/', update_load_document, name='update'),
    path('find/', search_engine, name='find'),
    path('details/<int:id>', get_details_product, name='details')

]
