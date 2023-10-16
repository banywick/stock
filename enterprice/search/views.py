from django.shortcuts import render, redirect
from .forms import DocumentForm
from .utils import save_data_db, delete_data_table
from .models import Remains
from .context_processors import get_context_input_filter_code,choice_project_dict, get_context_input_filter_all

def get_access(request):
    return render(request, 'registration.html')


def get_main_page(request):
    return render(request, 'main.html')


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
    return render(request, 'update.html', {'doc': doc})


def search_engine(request):  # Вьюшка под капотом с контекстым процессором.
    if request.method == 'POST':
        if str(request.POST['input']).startswith('*'):
            get_context_input_filter_code(request)
            return render(request, 'search.html')
        else:
            get_context_input_filter_all(request)
            return render(request, 'search.html')
    return render(request, 'search.html')


# else:  # Формируется 3 Q объекта. В импуте значения через пробел
#     projects_q = Q()  # Динамическое создание Q по выбранным проектам
#     for value in choice_project.values():
#         projects_q |= Q(**{'project': value})
#     values = str(user_send_value_input).split(' ')  # сбор значений с инпута
#     for i in enumerate(values):
#         d[i[0]] = i[1]
#     if not d.get(1):
#         d[1] = ''
#     if not d.get(2):
#         d[2] = ''
#     remains = Remains.objects.filter(projects_q).filter(Q(title__icontains=d[0])).filter(
#         Q(title__icontains=d.get(1))).filter(
#         Q(title__icontains=d.get(2))) | Remains.objects.filter(article__contains=user_send_value_input)
#     if not remains.exists():  # если ничего не найдено из нескольких значений в инпуте
#         context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
#                    'e_art_title': 'Товар не найден', 'project': choice_project.values(),  'file_name': file_name, 'username': request.user.username}
#         return render(request, 'search.html', context=context)
#     else:
#         context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
#                    'project': choice_project.values(), 'file_name': file_name, 'username': request.user.username}
#         return render(request, 'search.html', context=context,)


# return render(request, 'search.html',
#               {'title': 'Поиск', 'form': form, 'project': choice_project.values()})


def get_details_product(request, id):
    detail = Remains.objects.filter(id=id)
    for d in detail:
        article = d.article
        unit = d.base_unit
    det = Remains.objects.filter(article=article)
    sum_art = 0
    for d in det:
        sum_art += d.quantity
    sum_art = f'{sum_art}  {unit}'

    return render(request, 'details.html', {'title': 'детали', 'det': det, 'sum': sum_art, 'art': article})


def choice_projects(request):
    if request.method == 'POST':
        choice_project_dict(request)
        return redirect('find')
    return render(request, 'choice_project.html')
