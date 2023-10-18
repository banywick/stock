from ..utils_sql import get_doc_name

menu = [{'title': 'Главная', 'url_name': 'main'},
        {'title': 'Обновить базу', 'url_name': 'update'},
        {'title': 'Поиск', 'url_name': 'find'},
        ]


def get_all_context(request):
    return {'file_name': get_doc_name()[9:], 'menu': menu}
