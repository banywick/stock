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
            return redirect('find')
    return render(request, 'update.html', {'title': 'Обновление базы', 'menu': menu, 'doc': doc})


def search_engine(request):
    form = InputValue()
    if request.method == 'POST':
        d = {}
        form = InputValue(request.POST)
        user_value = request.POST['input']
        values = str(user_value).split(' ')
        for i in enumerate(values):
            d[i[0]] = i[1]
        if not d.get(1):
            d[1] = ''
        if not d.get(2):
            d[2] = ''
        remains = Remains.objects.filter(
            Q(title__icontains=d[0])).filter(Q(title__icontains=d.get(1))).filter(
            Q(title__icontains=d.get(2))) | Remains.objects.filter(article__contains=user_value)
        context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form}
        return render(request, 'search.html', context=context)

    return render(request, 'search.html', {'title': 'Поиск', 'menu': menu, 'form': form})


def get_details_product(request, id_prod):
    det = Remains.objects.filter(id=str(id_prod))
    return render(request, 'details.html', {'title': 'детали', 'det': det})
