from django.db import models


class Remains(models.Model):
    comment = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    article = models.CharField(max_length=30)
    party = models.CharField(max_length=9)
    title = models.CharField(max_length=100)
    base_unit = models.CharField(max_length=10)
    project = models.CharField(max_length=20)
    quantity = models.FloatField(blank=True)

    def __str__(self):
        return self.article, self.title


class Document(models.Model):
    document = models.FileField(upload_to='document', verbose_name='Выберите файл')
