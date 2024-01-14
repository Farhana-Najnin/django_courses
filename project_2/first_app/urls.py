from django.urls import path
#3ta way te import kora jai
#way-1
# from first_app.views import home
# way-2
# from first_app import views
# way-3
from . import views
urlpatterns = [
    path('',views.home),
    ]