from django.shortcuts import redirect, render

from .validators import validate_name_load_doc
from ..models import Remains, RemainsInventory, OrderInventory
from ..forms import InputValue, DocumentForm
from django.db.models import Q, Sum

from ..utils_sql import save_data_db

choice_project = dict()  # Хранилище выбранных проектов


def handle_uploaded_file(request):
    doc = DocumentForm(request.POST, request.FILES)
    error_massage = validate_name_load_doc(request)
    if not error_massage:
        try:
            doc.save()
            save_data_db()
        except IOError:
            error_massage = 'Произошла ошибка! Проверьте пожалуйта файл который вы загружаете. Ошибка'
    return doc, error_massage


def clear_sort(request):
    choice_project.clear()
    return redirect('find')


def choice_project_dict(request):  # Словарь из выбранных проектов
    all_project = Remains.objects.values_list('project',
                                              flat=True).distinct()  # переводит из картежа в список уникальные значения
    projects = request.POST.getlist('data_project')  # Выбор пользователя

    for i, project in enumerate(projects):
        choice_project[i] = project  # добавляем выбор в дикт
    return {'all_project': all_project, 'project': choice_project.values()}


def get_context_input_filter_all(request):  # Поиск всему
    form = InputValue(request.POST)
    if request.method == 'POST':
        input_str = str(request.POST['input'])
        if input_str.startswith('*'):  # поиск по коду
            query = Q(code__icontains=input_str[1:])
            error_message = 'Такой код не найден'
        elif input_str.startswith('-'):  # поиск по коментарию
            values = input_str[1:].split(' ')  # сбор значений с инпута по комменту
            values += [''] * (4 - len(values))  # Добавляем пустые строки, если введено менее четырех слов
            query = Q(comment__icontains=values[0]) & Q(comment__icontains=values[1]) & Q(comment__icontains=values[2]) & Q(
                comment__icontains=values[3])
            error_message = 'Такой коментарий не найден'
        else:
            values = input_str.split(' ')  # сбор значений с инпута
            values += [''] * (4 - len(values))  # Добавляем пустые строки, если введено менее четырех слов
            query = Q(title__icontains=values[0]) & Q(title__icontains=values[1]) & Q(title__icontains=values[2]) & Q(
                title__icontains=values[3])
            error_message = 'Товар не найден'
        print(input_str[1:])
        projects_filter_q = Q()
        for value in choice_project.values():
            projects_filter_q |= Q(**{'project': value})  # Динамическое создание Q по выбранным проектам
        remains = Remains.objects.filter(projects_filter_q).filter(query) | Remains.objects.filter(
            article__contains=input_str)
        if not remains.exists():  # если ничего не найдено из нескольких значений в инпуте
            return {'form': form, 'e_art_title': error_message}
        return {'remains': remains, 'form': form, 'project': choice_project.values()}
    return {'form': form, 'project': choice_project.values()}  # Возврат контест GET


def get_inventory(request):
    unic_sum_posit = RemainsInventory.objects.values('article', 'title', 'base_unit', 'status').annotate(
        total_quantity=Sum('quantity'))
    count_row = RemainsInventory.objects.values('article').distinct().count()  # количество уникальных строк
    not_empty_row = RemainsInventory.objects.filter(status='Сошлось').count()  # отмеченные как Сошлось
    remainder_row = count_row - not_empty_row
    percentage = f'{(not_empty_row / count_row) * 100:.2f}%'

    form = InputValue(request.POST)
    if request.method == 'POST':
        if request.POST.get('marker') == 'сошлось':
            inventory = RemainsInventory.objects.filter(status='Сошлось')
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
        if request.POST.get('marker') == 'в работе':
            inventory = RemainsInventory.objects.filter(status='В работе')
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
        if request.POST.get('marker') == 'перепроверить':
            inventory = RemainsInventory.objects.filter(status='Перепроверить')
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}
        if request.POST.get('input'):
            values = request.POST['input'].split(' ')  # сбор значений с инпута
            values += [''] * (4 - len(values))  # Добавляем пустые строки, если введено менее четырех слов
            query = Q(title__icontains=values[0]) & Q(title__icontains=values[1]) & Q(title__icontains=values[2]) & Q(
                title__icontains=values[3])
            error_message = 'Товар не найден'
            inventory = unic_sum_posit.filter(query) | unic_sum_posit.filter(
                article__contains=request.POST['input'])
            if not inventory.exists():  # если ничего не найдено из нескольких значений в инпуте
                return {'form': form, 'e_art_title': error_message}  # post если не найдено
            return {'form': form, 'inventory': inventory, 'count_row': count_row, 'not_empty_row': not_empty_row,
                    'remainder_row': remainder_row, 'percentage': percentage}  # post
    return {'form': form, 'count_row': count_row, 'not_empty_row': not_empty_row, 'remainder_row': remainder_row,
            'percentage': percentage}  # get


def get_one_product(article):
    return RemainsInventory.objects.filter(article=article).first()


def get_user_set_invent(product):
    return OrderInventory.objects.filter(product=product)


def get_total_quantity_ord(product):
    total = OrderInventory.objects.filter(product=product).aggregate(total=Sum('quantity_ord'))['total']
    return total if total is not None else 0


def get_unic_sum_posit(article):
    return RemainsInventory.objects.filter(article=article).aggregate(sum_art=Sum('quantity'))['sum_art']


def get_unic_sum_posit_remains_now(article):  # остаток по последнему загруженному документу
    if Remains.objects.filter(article__icontains=article).aggregate(sum_art_rem_now=Sum('quantity'))[
        'sum_art_rem_now'] == None:
        return 0
    return Remains.objects.filter(article__icontains=article).aggregate(sum_art_rem_now=Sum('quantity'))[
        'sum_art_rem_now']


def calculate_remains_sum(sum_remains_now, total_quantity_ord):  # Осталось посчитать
    if sum_remains_now == None:  # если нет позиции в таблице остатки (Remains)
        sum_remains_now = 0
    result = float(sum_remains_now) - float(total_quantity_ord)
    return result


def create_inventory_item(product, user, quantity_ord, address, comment):
    inventory_item = OrderInventory.objects.create(
        product=product,
        user=user,
        quantity_ord=quantity_ord,
        address=address,
        comment=comment)
    inventory_item.save()
