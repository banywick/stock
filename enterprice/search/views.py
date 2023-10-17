from django.shortcuts import render, redirect
from .forms import DocumentForm
from .utils import save_data_db, delete_data_table
from .models import Remains
from .context_processors import choice_project_dict


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
        return render(request, 'search.html')
    return render(request, 'search.html')


        




    #
    #     if str(request.POST['input']).startswith('*'):
    #         return render(request, 'search.html')
    #     else:
    #         return render(request, 'search.html')
    # return render(request, 'search.html')



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
