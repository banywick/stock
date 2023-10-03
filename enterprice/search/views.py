from django.shortcuts import render
from .forms import DocumentForm
from .utils import save_data_db, delete_data_table, get_doc_name,menu
from .models import Remains



def get_access(request):
    return render(request, 'registration.html')


def get_main_page(request):
    remains = Remains.objects.all()
    return render(request, 'base.html', {'title': 'Главная Страница', 'menu': menu, 'remains': remains })


def update_load_document(request):
    doc = DocumentForm()
    if request.method == 'POST' and request.FILES:
        doc = DocumentForm(request.POST, request.FILES)
        if doc.is_valid():
            doc.save()
            save_data_db()
            print('Удалили все данные')




    return render(request, 'update.html', {'title': 'Обновление базы', 'menu': menu, 'doc': doc})



