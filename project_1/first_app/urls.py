from django.urls import path
from . import views
urlpatterns = [
# from . import views--->avabe import korle nicer moto likhe dite hobe
    path('courses/',views.courses),
    path('about/',views.about),
    path('',views.home),
]
