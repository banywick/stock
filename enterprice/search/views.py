from django.db.models import Q
from django.db.models.functions import Cast
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
        if str(user_value).startswith('*'):
            remains = Remains.objects.filter(code__endswith=user_value[1:])
            if not remains.exists():
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                           'e_code': 'Такой код не найден'}
                return render(request, 'search.html', context=context)
            context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form}
            return render(request, 'search.html', context=context)
        else:
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
            if not remains.exists():
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                           'e_art_title': 'Товар не найден'}
                return render(request, 'search.html', context=context)
            else:
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form}
                return render(request, 'search.html', context=context)

    return render(request, 'search.html', {'title': 'Поиск', 'menu': menu, 'form': form})


def get_details_product(request, id):
    detail = Remains.objects.filter(id=id)
    for d in detail:
        article = d.article
        unit = d.base_unit
    det = Remains.objects.filter(article__contains=article)
    sum_art = 0
    for d in det:
        sum_art += d.quantity
    sum_art = f'{sum_art}  {unit}'

    return render(request, 'details.html', {'title': 'детали', 'det': det, 'sum': sum_art})
