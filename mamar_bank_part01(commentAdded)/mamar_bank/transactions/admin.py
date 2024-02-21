from django.contrib import admin
from .models import Transaction
# Register your models here.
# admin.site.register(Transaction)
@admin.register(Transaction) #admin panel e model admin use korte parbo ata deoa r por ->decoder bole atake->model admin use er jnno must ata use korte hoi
# admin panel k customizw korte j model use hoi setak bole model admin
class TransactionAdmin(admin.ModelAdmin):
    # list_display te jei sequence e dibo setai admin panel e show korbe
    list_display=['account','amount','balance_after_transaction','transaction_type','loan_approve']
    # jkn loan approve hobe tkn jate user er balance e seta add hoia jai sejnno 
    def save_model(self,request,obj,form,change):
        # filter dite pari->jate sudu loan approve jodi hoi sudu tkni jate hoi kaj gulo
        if obj.loan_approve==True:

            obj.account.balance += obj.amount
            obj.balance_after_transaction=obj.account.balance
        
            # balance update kore save
            obj.account.save()
            # super function jehetu override korsi sehetu bole dibo j vai ami tmr model ovverride korsi plz mairona
        super().save_model(request, obj,form,change)