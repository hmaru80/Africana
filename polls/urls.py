# djangotemplates/example/urls.py
from django.urls import reverse_lazy
from django.urls import  path
from django.contrib.auth import views as auth_views 
from .views import *
app_name = "polls"
# handler404 = 'error_404_view'

urlpatterns = [
    # path('', HomePageView.as_view(), name='homepage'), # Notice the URL has been named
    # path('about', Aboutpage, name="about"),
    path('', Homepage,name="home"),
    path('products', All_products,name="products"),
    path('contact', Contactus, name='contact'),
    path('signup', Signup, name='signup'),
    path('signin', Login_user, name='signin'),
    path('logout', Logout_user, name='logout'),
    path('users', user_list, name='users'),
    
    path('password/', auth_views.PasswordChangeView.as_view(success_url = reverse_lazy('polls:signin'),template_name='passwordreset.html'), name='reset'),    # path('password/', PasswordChangeView.as_view(template_name='passwordreset.html')),
    

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='passwordreset.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='passwordreset.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='passwordreset.html'
         ),
         name='password_reset_complete'),








    path('addproduct', AddProducts, name='addproduct'),
    path('productlist', Productlist, name='productlist'),
    path('productsearch', Productsearch, name='product-search'),
    path('productupdate/<int:productid>/', Updateproduct, name='update'),
    path('productdelete/<int:productid>/', Deleteproduct, name='delete'),
    path('addtocart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('emptycart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('viewproduct/<int:productID>/', ViewProduct, name='viewproduct'),
    path('viewcart',view_cart , name='viewcart'),
    path('info',some_view , name='info'),
    path('review',create_review , name='review'),
    
    path('addquantity/<int:product_id>/',increase_cart_item , name='addquantity'),
    path('reducequantity/<int:product_id>/',decrease_cart_item , name='reducequantity'),
   

    
]



