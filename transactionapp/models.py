
from django.db import models

from django.conf import settings


class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    current_balance = models.BigIntegerField()
    previous_balance = models.BigIntegerField()

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    CHOICES = (
        ('cr', 'Credit'),
        ('dr', 'Debit'),
        
    )


   

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='send_amount')
    receipent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receive_amount')
    amount = models.PositiveBigIntegerField(default=0)
    type = models.CharField(max_length=55, choices=CHOICES)
    schedule = models.BooleanField(default=False, )
    schedule_date = models.DateField(null=True, blank=True, )


    status = models.CharField(default='Pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, )



    def __str__(self):
        return f'{self.sender.username} transaction with {self.receipent.username}'





