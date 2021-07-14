from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=24)


class Operation(models.Model):
    PURCHASE = 'P'
    REFUND = 'R'
    WITHDRAWAL = 'W'
    OPERATIONS_CHOICES = (
        (PURCHASE, 'Purchase'),
        (REFUND, 'Refund'),
        (WITHDRAWAL, 'Withdrawal'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    transaction_id = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=24)
    created = models.DateTimeField()
    type = models.CharField(
        max_length=1,
        choices=OPERATIONS_CHOICES,
        default=WITHDRAWAL
    )

    def __str__(self):
        return f'{self.get_type_display()} - Amount: "{self.amount}" -' \
               f' {self.user.username}'
