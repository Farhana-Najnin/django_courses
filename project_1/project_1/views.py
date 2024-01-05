# import na korle error dekhabe 
from django.http import HttpResponse

# return obossoi dite hobe
def home(request):
    return HttpResponse("This is homepage")
def contact(request):
    return HttpResponse("This is contact")