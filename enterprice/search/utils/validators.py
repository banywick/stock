def validate_name_load_doc(request):  # Проверка расширения файла
    if not str(request.FILES['document']).endswith('.xlsx'):
        return 'Такой тип файла не поддерживается!! выберите файл .xlsx'
    return None
