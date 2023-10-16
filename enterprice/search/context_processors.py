from django.shortcuts import redirect

from .utils import get_doc_name
from .models import Remains
from .forms import InputValue
from django.db.models import Q

menu = [{'title': 'Главная', 'url_name': 'main'},
        {'title': 'Обновить базу', 'url_name': 'update'},
        {'title': 'Поиск', 'url_name': 'find'},
        ]

choice_project = dict()  # Хранилище выбранных проектов


def clear_sort(request):
    if request.method == 'POST':
        choice_project.clear()
        return redirect('find')


def choice_project_dict(request):  # Словарь из выбранных проектов
    projects = request.POST.getlist('data_project')  # Выбор пользователя
    for i in enumerate(projects):
        choice_project[i[0]] = i[1]  # добавляем выбор в дикт
    all_project = Remains.objects.values_list('project',
                                              flat=True).distinct()  # переводит из картежа в список уникальные значения
    context = {'all_project': all_project, 'project': choice_project.values()}
    return context


def get_all_context(request):
    return {'file_name': get_doc_name()[9:],
            'menu': menu,
            'username': request.user.username}


def get_context_input_filter_code(request):  # Поиск по коду с звездочкой
    form = InputValue(request.POST)
    if request.method == 'POST':
        user_send_value_input = request.POST['input']
        if str(user_send_value_input).startswith('*'):  # поиск по арикулу
            remains = Remains.objects.filter(code__endswith=user_send_value_input[1:])
            if not remains.exists():  # если кверисет пустой, ничего не найдено
                return {'form': form, 'e_code': 'Такой код не найден'}  # Контекст POST если значение  НЕ найдено
        # return {'remains': remains, 'form': form}  # Контест POST если значение найдено
    return {'form': form}  # Возврат контест GET


def get_context_input_filter_all(request):
    q_dict = {}
    user_send_value_input = request.POST['input']
    projects_filter_q = Q()  # Динамическое создание Q по выбранным проектам
    for value in choice_project.values():
        projects_filter_q |= Q(**{'project': value})
    values = str(user_send_value_input).split(' ')  # сбор значений с инпута
    for i in enumerate(values):
        q_dict[i[0]] = i[1]
    if not q_dict.get(1):
        q_dict[1] = ''
    if not q_dict.get(2):
        q_dict[2] = ''
    remains = Remains.objects.filter(projects_filter_q).filter(Q(title__icontains=q_dict[0])).filter(
        Q(title__icontains=q_dict.get(1))).filter(
        Q(title__icontains=q_dict.get(2))) | Remains.objects.filter(article__contains=user_send_value_input)
    if not remains.exists():  # если ничего не найдено из нескольких значений в инпуте
        return {'e_art_title': 'Товар не найден'}
    return {'remains': remains}
