from django import forms
from .models import Transaction

# transaction form aktai create korbo jetake inherit kore baki loan, withdraw er kaj ta korbo
class TransactionForm(forms.ModelForm):
    class Meta:
        model= Transaction
        field= ['amount','transaction_type']
    # user account pass kortesi
    def __init__(self, *args,**kwargs):
        # kwargs er modhe builtin kisu jinis pass kore dibo
        self.account=kwargs.pop('account')
        super.__init__(*args,**kwargs)
        # user deposit korte gele account capture kore nibo
        self.fields['transaction_type'].disabled=True #ei field disable thakbe
        self.fields['transaction_type'].widget=forms.HiddenInput() #user er theke hide kora thakbe
    def save(self,commit=True):
        # jkn akta object account create hosse tkn akta object er modhe self.account er data ta push kore dissi
        self.instance.account=self.account
        # transaction er por balance er tk balance_after_transaction e add hoia jabe
        # new balance dia update kore dibo
        self.instance.balance_after_transaction=self.account.balance #currently ase 0 tk ,tyle balance e add hobe 5000 jeheetu diposit korte casse 5000
        # self.instance.balance_after_transaction use kortesi karon loan neoar somoi jate direct loan er tk add hoia na jai age object e add hoi setar jnno
        return super().save()

# TransactionForm theke inherit kore kaj korbo jate aki kaj bar bar na kora lage



# kono form er field k update korte caile ba filter korte caile keyword - clean tarpor underscore(_)dia sei field name dibo
# example akane field name amount sejnno amra clean_amount disi
class DepositForm(TransactionForm):
    # clean_amount built in function
    # amount field k filter korbo
    def clean_amount(self):
        min_deposit_amount=100 #minimum 100 tk deposit korte hobe
        amount=self.cleaned_data.get('amount') #user er fillup kore form theke amount field er value k niye aslam,
        if amount<min_deposit_amount:
            #min_deposit_amount thekee soto hole error show korbe
            # raise error k show koranor jnno keyword
            # onk doroner errror thake setar modhe validationError akta
            # validation error er modhe onk error thake
            raise forms.ValidationError(
                # ai msg ta frontend e show hobe
                f'You need to deposit at least {min_deposit_amount} $'
            )
        # error asle return amount hbena
        return amount
    

class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account=self.account
        min_withdraw_amount=500
        max_withdraw_amount=20000
        balance=account.balance #user er balance 
        amount=self.cleaned_data.get('amount')
        if amount<min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )
        if amount>max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )
        if amount>balance:
            raise forms.ValidationError(
                f'You have { balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
        return amount
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount=self.cleaned_data.get('amount')
        return amount
    
# form er kaj form e korte hoi r class er kaj views e ata better