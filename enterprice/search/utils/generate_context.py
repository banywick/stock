from django.shortcuts import redirect
from ..models import Remains
from ..forms import InputValue
from django.db.models import Q

choice_project = dict()  # Хранилище выбранных проектов


def clear_sort(request):
    if request.method == 'POST':
        choice_project.clear()
        return redirect('find')


def choice_project_dict(request):  # Словарь из выбранных проектов
    all_project = Remains.objects.values_list('project',
                                              flat=True).distinct()  # переводит из картежа в список уникальные значения
    projects = request.POST.getlist('data_project')  # Выбор пользователя
    print(projects, '*******************')
    for i, project in enumerate(projects):
        choice_project[i] = project  # добавляем выбор в дикт
    return {'all_project': all_project, 'project': choice_project.values()}


def get_context_input_filter_all(request):  # Поиск всему
    form = InputValue(request.POST)
    if request.method == 'POST':
        input_str = str(request.POST['input'])
        if input_str.startswith('*'):  # поиск по арикулу
            query = Q(code__endswith=input_str[1:])
            error_message = 'Такой код не найден'
        elif input_str.startswith('-'):  # поиск по коментарию
            query = Q(comment__icontains=input_str[1:])
            error_message = 'Такой коментарий не найден'
        else:
            values = input_str.split(' ')  # сбор значений с инпута
            values += [''] * (4 - len(values))  # Добавляем пустые строки, если введено менее трех слов
            query = Q(title__icontains=values[0]) & Q(title__icontains=values[1]) & Q(title__icontains=values[2]) & Q(
                title__icontains=values[3])
            error_message = 'Товар не найден'

        projects_filter_q = Q()
        for value in choice_project.values():
            projects_filter_q |= Q(**{'project': value})  # Динамическое создание Q по выбранным проектам

        remains = Remains.objects.filter(projects_filter_q).filter(query) | Remains.objects.filter(
            article__contains=input_str)
        if not remains.exists():  # если ничего не найдено из нескольких значений в инпуте
            return {'form': form, 'e_art_title': error_message}
        return {'remains': remains, 'form': form}
    return {'form': form, 'project': choice_project.values()}  # Возврат контест GET
