from django.db import models
from django.contrib.auth.models import User


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


class RemainsInventory(models.Model):
    article = models.CharField(max_length=70, null=True)
    title = models.TextField(null=True)
    base_unit = models.CharField(max_length=10, null=True)
    quantity = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.article}{self.title}{self.base_unit}{self.quantity}'


class OrderInventory(models.Model):
    product = models.ForeignKey(RemainsInventory, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_ord = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'OrderInventory (id: {self.id}, product: {self.product.title} {self.product.article} {self.total_quantity}'
