from ..utils_sql import get_doc_name


def get_all_context(request):
    return {'file_name': get_doc_name()[9:]}



def user_permission_is_in_group(request):
    user_is_in_group = request.user.groups.filter(name='link_inventary').exists()
    return {'user_is_in_group': user_is_in_group}

