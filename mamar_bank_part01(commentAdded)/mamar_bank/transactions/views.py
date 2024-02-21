from django.shortcuts import render
from django.views.generic import CreateView,ListView,View
# jate keo login na kore page e dukte na pare aijnno LoginRequiredMixin use korbo amra
from django.contrib.auth.mixins import LoginRequiredMixin
# amader model aktai transaction
from .models import Transaction
# deposit,withdraw form inherit korbo 
from .forms import DepositForm,WithdrawForm,LoanRequestForm
# transaction type select korar jnno type gula inherit kortesi 
from .constants import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
# Create your views here.

# createview use korbo -->multiple kaj korar option dibe
# common classed based view create korbo jeta inherit kre sobai kaj korbe

# common template create korbo jate ai view k inherit kore amra deposit ,withdraw,loan request er kaj korbo
# jate keo login na kore page e dukte na pare aijnno LoginRequiredMixin use korbo amra

class TransactionCreateView(LoginRequiredMixin,CreateView):
    template_name=''
    # form ta antese model
    model= Transaction
    # title built in na ty nice get_context_data dia pass korabo context akare
    title=''
    success_url=reverse_lazy('transaction_form.html')
    # jkni kono form er object hobe tkni get_form er kaj ta kokrte hobe
    # constructor er madhome form e data pass
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account, #user er account acces kore rakhtese account e
        })
        return kwargs
        # upore labh ta hosse account er value ta pass kore dissi models.py er Transaction er __init__ funtion e,
        # sekhane pop hoia user type dekhbe disable kora(ata amra fill up korbo). Then submit button click korle mane
        #  save korte caile account ta caption kore balance ta ber kore ane balance_after transaction dia protita bar update kore dissi..
        # super().save() ->mane parent j silo built in, seta override kore kore save kore dissi
    # context forntend e set kore dissi
    def get_context_data(self,**kwargs):
        # class theke builtin context nia asbo jekane normally kono falue thakbena setake amra override korbo
        context=super().get_context_data(**kwargs)
        context.update({
            # pass kore dibo
            # TransactionCreateViewform ta keo access korle sathe sathe context akare title e template akare pass hoi jabe-->jehetu title builtin na ty aavbe context akare patahbo
            'title' : self.title
        })
        return context

# jehetu akane TransactionCreateView k inherit kora hoise ty auto login kora sara keo page ta access korte parbena inherit korar karone
        # form ta sobar jnno different thaaki sudu form tar kaj e alada alada korbo
class DepositMoneyView(TransactionCreateView):
    form_class= DepositForm
    # title pass hoia jabe TransactionCreateView e
    title= "Deposit"
    # user sudu title dekhte parbe kintu select korte parbena seta amra handle korbo akane
    # transactiontype ta akane handle korbo
    # return the initial data to use for form on this view
    # user form ta submit korar agei initially data push kore  dibo
    # transaction type ta user select korte parbena backend theke ai gulo amra select kore dissi 
    def get_initial(self):
        # initial er jaigai onno nam dileo somossa nai
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    # if form_valid er kaj tai form_valid function ta kore
    def form_valid(self,form):
        # chaknite chakar por j data passi seta nissi
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        # balance update korte parbo
        # user er kase ase 500,jodi deposit kori 1000,tyle akane ase update hoia user baalance hobe 1500 tk
        account.balance+=amount
        # data save korbo
        account.save(
            # kake update korsi seta bole dibo save er jnno
            update_fields = ['balance']
        )
        # form fillup hoia gese sejnno akn message dibo
        messages.success(self.request,f"{amount}$ was deposited to you account successfully")
        # super call kore form jeta silo setake amra override kore fellm
        return super().form_valid(form)
    


class WithdrawMoneyView(TransactionCreateView):
    form_class= WithdrawForm
    # title pass hoia jabe TransactionCreateView e
    title= "Withdraw Money"
    # user sudu title dekhte parbe kintu select korte parbena seta amra handle korbo akane
    # transactiontype ta akane handle korbo
    # return the initial data to use for form on this view
    # user form ta submit korar agei initially data push kore  dibo
    # transaction type ta user select korte parbena backend theke ai gulo amra select kore dissi 
    def get_initial(self):
        # initial er jaigai onno nam dileo somossa nai
        initial = {'transaction_type': WITHDRAWAL}
        return initial
    
    # if form_valid er kaj tai form_valid function ta kore
    def form_valid(self,form):
        # chaknite chakar por j data passi seta nissi
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        # balance update korte parbo
        # user er kase ase 1500,jodi withdraw kori 1000,tyle akane ase update hoia user baalance hobe 500 tk
        account.balance-=amount
        # data save korbo
        account.save(
            # kake update korsi seta bole dibo save er jnno
            update_fields = ['balance']
        )
        # form fillup hoia gese sejnno akn message dibo
        messages.success(self.request,f"Successfully withdrawn {amount}$ from your account")
        # super call kore form jeta silo setake amra override kore fellm
        return super().form_valid(form)
    

    


class LoanRequestView(TransactionCreateView):
    form_class= LoanRequestForm
    # title pass hoia jabe TransactionCreateView e
    title= "Request for loan"
    def get_initial(self):
        # initial er jaigai onno nam dileo somossa nai
        initial = {'transaction_type': LOAN}
        return initial
    
    # if form_valid er kaj tai form_valid function ta kore
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        # amra chai akjn user 3barer besi jate loan na nite pare
        # LOAN ba 3 jai dei kaj korbe
        # account jodi request.user.account hoi ,loan type hoi, r loan approve field ta true thakle tkn count korbo--->mainly kotogula loan hoise seta count kortesi
        current_loan_count=Transaction.objects.filter(account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        if current_loan_count>=3:
            return HttpResponse("You Have crossed your limit")
        messages.success(self.request,f"loan request for {amount} $ has been successfully sent to admin")
        # super call kore form jeta silo setake amra override kore fellm
        return super().form_valid(form)
    
# total jotogula transition ase ba post ase segulok akbare dekanoke bole--> list view
    # single value k single block e details e show korake bole-->details view
class TransactionReportView(LoginRequiredMixin,ListView):
    template_name="transactions/transaction_report.html"
    model= Transaction
    balance=0
    context_object_name= "report_list"

    # website e 2ta request kora jai --> get request,post request.
    # get request url er madhome get kori ,sekhane parameter pass korte hoi
    # post request e kono parameter pass kora lage na
    def get_queryset(self):
        # jodi user kono type filter na kore taile tar total transaction report dekhabo
        # get_querysete r parent k override korbo sejnno super
        # bole dissi j query set er modhe data gula thakbe r ki
        queryset=super().get_qureryset().filter(
            # kon user er account seta filter kore nibo
            account=self.request.user.account
        ) #quryset k apatoto filter kore rakhtesi account k

        # start_date string format e nite hobe karon jkn url e get kore tkn string format e get kore
        start_date_str=self.request.GET.get('start_date')
        end_date_str=self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            # string date guloke date e convert korte hobe...strptime function nuse korbo jeta datetime object return kore+ datetime object import korte hbe + last e format kmn cassi seta dite hobe
            start_date=datetime.strptime(start_date_str , "%Y-%m-%d").date()
            end_date=datetime.strptime(end_date_str , "%Y-%m-%d").date()

            # queryset er account theke date dia filter korbo
            # timestamp_date_gte mane timestamp theke j date pabo seta getter than 
            # timestamp_date_lte mane timestamp theke j date pabo seta less than 
            queryset=queryset.filter(timestamp__date__gte =start_date,
                                     timestamp__date__lte =end_date,)
            # jodi avabe queryset age account nia filter korte asubidha hoi tahole atao kora jai ---> Transaction.objects.get(account=request.self.user.account) kore filter kore then time er upore filter korbo--setai akn korbo
            # jkn multiple function model e use korte hai tkn use korbo aggregate
            # Sum inherit korte hobe 
            # Sum(account) theke format return korbe account__sum
            self.balance=Transaction.objects.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            # filter na hole user er ja balance silo setai show korbe
            self.balance=self.request.user.account.balance
        # unique queryset nibo ty distinct->ata na dileo hoi
        return queryset
    # context er khisebe pass korbo account k
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
           'account' : self.request.user.account
        })
        return context


class PayLoanView(LoginRequiredMixin,View):
    def get(self,request,loan_id):
        # jodi loan_id er kaok pai tyle dekhabe noile error dibe 404
        # id built in vabe create hoi
        loan=get_object_or_404(Transaction,id=loan_id)
        # akjn user loan pay korte parbe tkni jkn tar loan request approve hobe
        if loan.loan_approve:
            user_account = loan.account #karon transaction er modhei user account thakbe
            if loan.amount<user_account.balance:
                user_account.balance-=loan.amount
                loan.balance_after_transaction=user_account.balance
                # user account er kaj save korlm
                user_account.save()
                loan.transaction_type=LOAN_PAID
                # loan tao save kore feellmm
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(self.request,f'Loan amount us greater than available balance')
                return redirect('loan_list')
            

# loan guloke list akare dekhate chai ty list view
class LoanListView(LoginRequiredMixin,ListView):
    model=Transaction
    template_name="transactions/loan_request.html"
    # context_object_name ata na dile Transactions,object dia access kora jaito
    context_object_name= "loans"

    def queryset(self):
        user_account=self.request.user.account

        queryset= Transaction.objects.filter(account=user_account,transaction_type=LOAN)
        return queryset