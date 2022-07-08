from datetime import datetime
from django.db import models
from django.conf import settings

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    trans_id = models.CharField(max_length=50, null=True)
    trans_ref = models.CharField(max_length=50, null=True)
    trans_status = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add =True)
    updated = models.DateTimeField(auto_now =True)
    # amount = models.FloatField(default=1)
    
    
    def __str__(self):
        return self.trans_ref
