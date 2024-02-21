from django.db import models
# UserBankAccount e j balance silo seta lagbe sejnno import korbo
from accounts.models import UserBankAccount
# Create your models here.
from .constants import TRANSACTION_TYPE
class Transaction(models.Model):
    # akjn user er multiple account(savings,current) thaktei pare sejnno one to many relationshiop hobe
    account=models.ForeignKey(UserBankAccount, related_name='transactions',on_delete=models.CASCADE)    #akjn user er multiple transaction hote pare
    amount=models.DecimalField(decimal_places=2,max_digits=12)
    balance_after_transaction=models.DecimalField(decimal_places=2,max_digits=12)
    transaction_type=models.IntegerField(choices=TRANSACTION_TYPE,null= True)
    # akjn user kokn transaction kortese sei time track rakhte
    timestamp=models.DateTimeField(auto_now_add=True) #jkn akta transaction object create hobe tkni store korbe time
    # user loan nile seta backend theke approve korte hobe setar jnno loan_approve
    loan_approve=models.BooleanField(default=False)
    class Meta:
        # time tar upore amar transeaction sort korbo
        ordering=['timestamp']