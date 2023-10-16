from django.db import models


class Remains(models.Model):
    comment = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    article = models.CharField(max_length=30, null=True)
    party = models.CharField(max_length=9, null=True)
    title = models.CharField(max_length=100, null=True)
    base_unit = models.CharField(max_length=10, null=True)
    project = models.CharField(max_length=20, null=True)
    quantity = models.FloatField(blank=True, null=True)


class Document(models.Model):
    document = models.FileField(upload_to='document', verbose_name='Выберите файл')
