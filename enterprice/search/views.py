from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import DocumentForm, InputValue
from .utils import save_data_db, delete_data_table, menu
from .models import Remains

choice_project = dict()


def clear_sort(request):
    if request.method == 'POST':
        choice_project.clear()
        return redirect('find')


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
        user_send_value_input = request.POST['input']

        if str(user_send_value_input).startswith('*'):  # поиск по арикулу
            remains = Remains.objects.filter(code__endswith=user_send_value_input[1:])
            if not remains.exists():  # если кверисет пустой, ничего не найдено
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                           'e_code': 'Такой код не найден', 'project': choice_project.values()}
                return render(request, 'search.html', context=context)
            context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                       'project': choice_project.values()}
            return render(request, 'search.html', context=context)
        else:  # Формируется 3 Q объекта. В импуте значения через пробел
            projects_q = Q()  # Динамическое создание Q по выбранным проектам
            for value in choice_project.values():
                projects_q |= Q(**{'project': value})

            values = str(user_send_value_input).split(' ')

            # for i in enumerate(values):
            #     print(i)
            #     d[i[0]] = i[1]
            # if not d.get(1):
            #     d[1] = ''
            # if not d.get(2):
            #     d[2] = ''

            titles_q = {i: v for i, v in enumerate(values)}  # Перевел список в дикт с ключами цифрами
            print(titles_q)
            remains = Remains.objects.filter(Q(title__icontains=titles_q.get(0))).filter(
                Q(title__icontains=titles_q.get(1)) | '')

            # remains = Remains.objects.filter(projects_q).filter(Q(title__icontains=d[0])).filter(
            #     Q(title__icontains=d.get(1))).filter(
            #     Q(title__icontains=d.get(2))) | Remains.objects.filter(article__contains=user_send_value_input)

            if not remains.exists():  # если ничего не найдено из нескольких значений в инпуте
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                           'e_art_title': 'Товар не найден', 'project': choice_project.values()}

                return render(request, 'search.html', context=context)
            else:
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                           'project': choice_project.values()}
                return render(request, 'search.html', context=context)

    return render(request, 'search.html',
                  {'title': 'Поиск', 'menu': menu, 'form': form, 'project': choice_project.values()})


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


def choice_projects(request):
    if request.method == 'POST':
        projects = request.POST.getlist('data_project')
        for i in enumerate(projects):
            choice_project[i[0]] = i[1]
        return redirect('find')
    all_project = Remains.objects.values_list('project', flat=True).distinct()
    context = {'title': 'Проект', 'all_project': all_project}
    return render(request, 'choice_project.html', context)
