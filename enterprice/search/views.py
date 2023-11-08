import copy

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm
from .utils_sql import save_data_db
from .models import Remains, OrderInventory, RemainsInventory
from .utils.generate_context import get_context_input_filter_all, choice_project_dict, get_inventory, get_one_product, \
    get_user_set_invent, get_total_quantity_ord, get_unic_sum_posit, calculate_remains_sum, create_inventory_item, \
    handle_uploaded_file, get_unic_sum_posit_remains_now
from .utils.validators import validate_name_load_doc
from django.urls import reverse


def user_logout(request):
    logout(request)
    return redirect('login')


def get_access(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('find')
        else:
            context['error'] = 'Неверное имя пользователя или пароль'
    if request.user.is_authenticated:
        return redirect('find')
    return render(request, 'registration.html', context)


def get_main_page(request):
    return render(request, 'main.html')


@login_required
def update_load_document(request):
    doc = DocumentForm()
    error_massage = ''
    if request.method == 'POST' and request.FILES:
        doc, error_massage = handle_uploaded_file(request)
        if not error_massage:
            return redirect('find')
        else:
            messages.error(request, error_massage)
    else:
        messages.error(request, error_massage)
    return render(request, 'update.html', {'doc': doc, 'error_massage': error_massage})


@login_required
def search_engine(request):
    context = get_context_input_filter_all(request)
    return render(request, 'search.html', context=context)


@login_required
def get_details_product(request, id):
    detail = Remains.objects.filter(id=id)
    for d in detail:
        article = d.article
        unit = d.base_unit
        title = d.title
    det = Remains.objects.filter(article=article)
    sum_art = []
    for d in det:
        sum_art.append(float(d.quantity))
    sum_art = f'{sum(sum_art)}  {unit}'
    return render(request, 'details.html',
                  {'title': 'детали', 'det': det, 'sum': sum_art, 'art': article, 'title': title})


@login_required
def choice_projects(request):
    context = choice_project_dict(request)
    if request.method == 'POST':
        return redirect('find')
    return render(request, 'choice_project.html', context=context)


def get_main_inventory(request):
    context = get_inventory(request)
    return render(request, 'inventory.html', context=context)


def inventory_detail(request, article):
    product = get_one_product(article)  # выбор первой позицци по артикулу для детализации
    user_set_invent = get_user_set_invent(product)  # Фильтрация по выбору для всех пользователей
    total_quantity_ord = get_total_quantity_ord(product)  # Посчитанно всеми пользователями
    unic_sum_posit = get_unic_sum_posit(article)  # Остаток по инвентаризации

    sum_remains_now = "{:.2f}".format(get_unic_sum_posit_remains_now(article))  # Текущий остаток
    sum_remains_now = float(sum_remains_now)  # пеобразование 2 знака после точки
    move_product = float(sum_remains_now) - float(
        unic_sum_posit)  # текущий остаток минус остаток инвентаризации (движение)
    move_product = "{:.2f}".format(move_product)
    remains_sum = calculate_remains_sum(sum_remains_now,
                                        total_quantity_ord)  # тек остаток минус сумма подсчета пользователями (Движение)

    if request.method == 'POST':
        quantity_ord = request.POST.get('quantity_set')
        set_address = request.POST.get('address')
        set_comment = request.POST.get('comment')
        user = request.user

        create_inventory_item(product, user, quantity_ord, set_address, set_comment)
        return HttpResponseRedirect(reverse('inventory_detail', args=(article,)))
    get_status = RemainsInventory.objects.filter(article=article).first().status

    context = {'product': product, 'user_set_invent': user_set_invent,
               'total_quantity_ord': total_quantity_ord, 'unic_sum_posit': unic_sum_posit, 'remains_sum': remains_sum,
               'sum_remains_now': sum_remains_now, 'move_product': move_product, 'get_status':get_status}
    return render(request, 'inventory_detail.html', context=context)


def user_detail(request):
    order = OrderInventory.objects.select_related('product').filter(user=request.user)
    return render(request, 'user_detail.html', {'order': order})


def delete_row(request, id_row):
    order = OrderInventory.objects.get(id=id_row)
    order.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def set_status(request, status, article):
    RemainsInventory.objects.filter(article=article).update(status=status)

    return redirect('inventory_detail', article=article)
