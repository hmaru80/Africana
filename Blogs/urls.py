from django.urls import path
from .views import Aboutus,Reviews,Pay_here,Your_invoice
from polls.models import Review
app_name = 'Blogs'


urlpatterns = [
    path ("", Reviews, name="blogs"),
    path('payment',Pay_here, name='checkout'),
    path("about",Aboutus, name="about"),
    path("invoice",Your_invoice, name="invoice"),
    
]