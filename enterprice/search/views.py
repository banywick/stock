from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import DocumentForm, InputValue
from .utils import save_data_db, delete_data_table, menu
from .models import Remains


def get_access(request):
    return render(request, 'registration.html')


def get_main_page(request):
    return render(request, 'base.html', {'title': 'Главная Страница', 'menu': menu})


def update_load_document(request):
    doc = DocumentForm()
    if request.method == 'POST' and request.FILES:
        doc = DocumentForm(request.POST, request.FILES)
        if doc.is_valid():
            doc.save()
            delete_data_table()
            save_data_db()
            print('Данные загружены')
            return redirect('main')
    return render(request, 'update.html', {'title': 'Обновление базы', 'menu': menu, 'doc': doc})


def search_engine(request):
    form = InputValue()
    if request.method == 'POST':
        form = InputValue(request.POST)
        user_value = request.POST['input']
        remains = Remains.objects.filter(
            Q(title__icontains=user_value) |
            Q(title__istartswith=user_value) |
            Q(title__iendswith=user_value) |
            Q(article__endswith=user_value) |
            Q(article__contains=user_value))

        context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form}
        return render(request, 'search.html', context=context)
    return render(request, 'search.html', {'title': 'Поиск', 'menu': menu, 'form': form})
