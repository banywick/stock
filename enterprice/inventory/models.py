from django.db import models
from django.contrib.auth.models import User


class InventoryStatic(models.Model):
    article = models.CharField(max_length=50, null=True)
    title = models.TextField(null=True)
    base_unit = models.CharField(max_length=10, null=True)
    quantity = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    status = models.CharField(max_length=15)







#
# result = models.DecimalField(max_digits=4,decimal_places=2)
#     date_time = models.DateTimeField(auto_now_add=True)
#     comment = models.TextField()
#     status = models.CharField(max_length=15)
#     address = models.CharField(max_length=15)