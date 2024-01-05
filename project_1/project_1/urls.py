
from django.contrib import admin
# first_app/ jate website e include kora jai ty include import kore path e add kore dibo
from django.urls import path,include
# view.py theke contact import kortesi
# from views import contact -->avabeo kora jai import
# jehetu views project folder r aki folder er modhei import er kaj korsi ty avabeo likha jai
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # homepage er khetre
    path("",views.home),
    # include must dite hobe-->app er under e separate urls separate huge function kaj korate cai
    # jotogula app toiri korbo sobgular under e urls thakuk caile janai dite hobe include dia
    path("first_app/", include("first_app.urls")),
# from . import views--->avabe import korle nicer moto likhe dite hobe ...r contact er last e \ must dite hobe
    path('contact/',views.contact),
    
]
