from django.db import models


class Remains(models.Model):
    comment = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    article = models.CharField(max_length=50, null=True)
    party = models.CharField(max_length=9, null=True)
    title = models.TextField(null=True)
    base_unit = models.CharField(max_length=10, null=True)
    project = models.CharField(max_length=30, null=True)
    quantity = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)







class Document(models.Model):
    document = models.FileField(upload_to='document', verbose_name='Загрузить документ')


