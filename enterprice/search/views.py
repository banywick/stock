from django.shortcuts import render, redirect
from .forms import DocumentForm
from .utils_sql import save_data_db, delete_data_table
from .models import Remains
from .utils.generate_context import get_context_input_filter_all, choice_project_dict


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
            return redirect('find')
    return render(request, 'update.html', {'doc': doc})


def search_engine(request):
    context = get_context_input_filter_all(request)
    return render(request, 'search.html', context=context)


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
    context = choice_project_dict(request)
    if request.method == 'POST':
        return redirect('find')
    return render(request, 'choice_project.html', context=context)
