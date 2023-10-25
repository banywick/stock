from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .utils_sql import load_inventory_doc
from .models import Remains
from .utils.generate_context import get_context_input_filter_all, choice_project_dict, get_inventory, get_doc_name
from .utils.validators import validate_name_load_doc


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
    doc = None
    error_massage = ''
    if request.method == 'POST' and request.FILES:
        doc = DocumentForm(request.POST, request.FILES)
        error_massage = validate_name_load_doc(request)
        if not error_massage:
            try:
                doc.save()
                get_doc_name()
                return redirect('find')
            except IOError:
                messages.error(request, 'Произошла ошибка! Проверьте пожалуйта файл который вы загружаете. Ошибка')
                return render(request, 'update.html', {'doc': doc})
    else:
        doc = DocumentForm()
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