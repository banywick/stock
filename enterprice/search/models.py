from django.db import models
from .utils import menu, get_doc_name


class RemainsManager(models.Manager):

    def user_find_code(self, user_send_value_input, form):
        if str(user_send_value_input).startswith('*'):  # поиск по арикулу
            remains = Remains.objects.filter(code__endswith=user_send_value_input[1:])
            context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                       'file_name': get_doc_name()[9:], }
            if not remains.exists():  # если кверисет пустой, ничего не найдено
                context = {'title': 'Поиск', 'menu': menu, 'remains': remains, 'form': form,
                           'file_name': get_doc_name()[9:], 'e_code': 'Такой код не найден'}
                return context
        return context




class Remains(models.Model):
    comment = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    article = models.CharField(max_length=30, null=True)
    party = models.CharField(max_length=9, null=True)
    title = models.CharField(max_length=100, null=True)
    base_unit = models.CharField(max_length=10, null=True)
    project = models.CharField(max_length=20, null=True)
    quantity = models.FloatField(blank=True, null=True)
    objects = RemainsManager()


class Document(models.Model):
    document = models.FileField(upload_to='document', verbose_name='Выберите файл')
