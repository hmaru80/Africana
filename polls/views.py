# djangotemplates/example/views.py
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import render, redirect
from django.views.generic import TemplateView # Import TemplateView
from .models import Product,CartItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import admin   
from .forms import RegistrationForm, NewProduct,Rating
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseNotFound

# def error_404_view(request, exception):
#     return HttpResponseNotFound("go home")

   
    
    


@login_required(login_url='polls:signin')
def create_review(request):
        user =request.user
        
        if request.method == 'POST':
            
            form = Rating(request.POST,)
            if form.is_valid():
                    reviewform= form.save(commit=False)
                    reviewform.reviewer=user 
                    form.save()
            messages.success(request,"product reviewed successfully")       
            return redirect('polls:home')
        else:
            form = Rating()
            return render(request, 'review.html',{'form':form} )





def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    cart = CartItem.objects.all()
    total_price = (item.quantity * item.product.price for item in cart)
    y = 750
    for item in cart:
        p.drawString(100, y, item.product.name)
        p.drawString(250, y, str(item.quantity))
        p.drawString(350, y, str(item.product.price))
        p.drawString(450, y, str(total_price))
        y -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="africana-invoice.pdf")






@login_required(login_url='polls:signin')
def Pay_here(request):
        
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        return render(request,'checkout.html' ,{'cart_items':cart_items , 'total_price':total_price})

@login_required(login_url='polls:signin')
def decrease_cart_item(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    user = request.user
    
    cart_item= CartItem.objects.get(product=product , user=user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.success(request, 'Product removed')
    return redirect('polls:viewcart')

@login_required(login_url='polls:signin')
def increase_cart_item(request, product_id):
    user=request.user
    product = get_object_or_404(Product, pk=product_id)

    try:
        cart_item = CartItem.objects.select_for_update().get(product=product, user=user)
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1)
    else:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('polls:viewcart')
            

# Create a view to add a product to the cart.
@login_required(login_url='polls:signin')
def add_to_cart(request, product_id):
    # Get the product from the database.
    product = get_object_or_404(Product, id=product_id)
    # Add the product to the cart.
    
    
    cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    
    
    messages.success(request, 'Product added successfully to cart')
    return redirect('polls:home')

# Create a view to remove a product from the cart.
@login_required(login_url='polls:signin')
def remove_from_cart(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    # cart = CartItem.objects.filter( id=product_id)
    items = CartItem.objects.get(product=product, user= request.user)
   
    items.delete()

    
    messages.success(request, 'Product removed successfully from cart')
    # Redirect the user to the cart page.
    return redirect('polls:viewcart')



# cart.save()



# Create a view to view the cart.
@login_required (login_url='polls:signin')
def view_cart(request):
    
    # Get the cart for the current user.

    
    contents= CartItem.objects.filter(user =request.user)
    # breakpoint()

   
    total_price = sum( item.quantity * item.product.price for item in contents )

    
    

    return render(request, 'invoicing.html', {'contents':contents,'total_price':total_price})
    










def Productsearch(request):
    if request.method == 'POST':
        searched= request.POST['search']
        item=Product.objects.filter(name__contains=searched)
        # messages.success(request, ('Is this what you were looking for?'))
        return render(request, 'productsearch.html',{'search':searched,'item':item})
    else:
        return render(request, 'productsearch.html')


@login_required(login_url='polls:signin')
def Productlist(request):
    user= request.user
    merchantgroup=user.groups.all() #lists all the groups
    group_names = []
    for group in merchantgroup:   
        group_names.append(group.name)
    products = Product.objects.filter(owner =request.user)   
    return render(request, 'productlist.html',{'products': products, 'group_names':group_names}, )


# Delete function
@login_required(login_url='polls:signin')
def Deleteproduct(request,productid):
    Erase=Product.objects.get(id=productid)
    Erase.delete()
    messages.success(request, ('You have deleted the product successfully !!!!!!'))
    return redirect('polls:productlist')

# Update function
@login_required(login_url='polls:signin')
def Updateproduct(request ,productid):
    update=Product.objects.get(id=productid)
    if request.method == 'POST':
        form=NewProduct(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, ('Product updated successfully'))
            return redirect('polls:productlist')
    form= NewProduct(instance=update)
    return render(request, 'product-update.html', {'form':form , 'productid':productid })
    

def AddProducts(request): 
    form= NewProduct
    user= request.user
    merchantgroup=user.groups.all() #lists all the groups
    group_names= [group.name for group in merchantgroup] #creates a loop to check for a group name
    # group_names = []
    # for group in merchantgroup:   
    #      group_names.append(group.name)
    if request.method == 'POST':
        form = NewProduct (request.POST or None , files = request.FILES,)
        if form.is_valid():
            productform= form.save(commit=False)
            productform.owner=user   

            form.save()
            messages.success(request, ('Product added successfully'))
            
            return redirect('polls:addproduct')

    else:
         form =NewProduct()      
    return render(request, 'merchant.html',{'form': form, 'group_names':group_names})
    



def All_products(request):
    user= request.user
    product_list = Product.objects.all()
    merchantgroup=user.groups.all() #lists all the groups
    group_names= [group.name for group in merchantgroup]

    return render(request, 'homepage.html', {'product_list': product_list,'group_names':group_names})


def Homepage(request):
    random_products = Product.objects.order_by('?')[:3]
    return render (request,'welcome.html',{'random_products':random_products})



def Contactus(request):
    
    return render(request,'contact.html')


def Signup(request):
    
    if request.method == 'POST': 
     form = RegistrationForm(request.POST)
     if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username = username, password=password)
            login(request, user)
            
           

            messages.success(request, ('Login successfull '))
            return redirect( 'polls:home')
    else:
            form = RegistrationForm()
            
    return render(request,"signup.html",{
         'form':form,
         })


def Login_user(request):
    if request.method =='POST':
    
        username = request.POST["Username"]
        password = request.POST["password"]
        # email = request.POST["email"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                if user.groups.filter(name='Merchant').exists():
                    return redirect ( 'polls:addproduct')
                elif user.groups.filter(name='Support').exists():
                     return redirect ('tasks:task_list')
                return redirect( 'polls:home')
        
        else:
                messages.info(request , ("User does not exist!"))
                return render (request, 'signin.html')
            
    return render (request, 'signin.html')



def Logout_user(request):
    logout(request)
    messages.info(request , ("User logged out successfully"))
    return render(request, "signin.html")
    
    
    
    
def user_list(request):
    users = User.objects.all()
    item = CartItem.objects.filter().order_by('user')
    # users = User.objects.all()
    # cart_items = {}

    # for user in users:
    #     cart_items[user] = CartItem.objects.filter(user=user).order_by('user')



    return render(request, 'card-hover.html', {'users': users ,'item':item})   
    # return render(request, 'card-hover.html', {'users': users ,'cart_items':cart_items})



   
   


    # subject = 'Hello'
    # message = 'This is a test email.'
    # from_email = 'your_email@gmail.com'
    # recipient_list = ['recipient_email@gmail.com', ]

    # send_mail(subject, message, from_email, recipient_list)






# Addto cart
        # def add_to_cart(request, product_id):
        #     product = Product.objects.get(pk=product_id)
        #     cart = Cart.objects.get_or_create(user=request.user)
        #     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        #     if  item_created:
        #         cart_item.quantity += 1
        #         cart_item.save()
        #         messages.success(request, ('Product added to cart'))
        #         return redirect('polls:home')
        #     else:
        #         Cart.objects.create(user=request.user, product=product_id)
        #         messages.success(request, "Item added to your cart.")
        #         return redirect('polls:home',{'cart_item':cart_item, 'product_id':product_id,'product':product})


#manual form creation code

        # username=request.POST.get('Username')
        # email=request.POST.get('email')
        # password=request.POST.get('password')
        # p=Shopper(email=email, name=username, password=password)     #left models right views input
        # p.save()
        # return render(request, 'homepage.html')   
          
        # <div class="signup-form">
        #     <form action="{% url 'polls:signup' %}" method="post" >
        #         {% csrf_token %}
        #         <label for="Username">Your name</label><br>
        #         <input type="text" name="Username" id="" placeholder="your username">
                
                

                
        #         <br><br>
        #         <label for="email">Your email</label><br>
        #         <input type="email" name="email" id="" placeholder="type email">
                
                
        #         <br><br>
        #         <label for="password">Enter Password</label><br>
        #         <input type="password" name="password" placeholder="Secret password">
        #         <br><br>

                
                
        #         <!-- <textarea cols="30" rows="10"></textarea> -->
        #         <input type="submit" value="Register">
        #         <p style="padding: 1px; font-weight: 600;" >Already have an account?</p>
        #         <a href="{% url 'polls:signin'%}">Login</a>
        #     </form> <br>

            
            
        # </div>
# def add_product_to_cart(product_id, quantity):

#     # Check if the product exists in the cart.
#     if product_id in cart:
#         # If the product exists, increment the quantity.
#         cart[product_id]['quantity'] += quantity
#     else:
#         # If the product does not exist, add it to the cart.
#         cart[product_id] = {'quantity': quantity}


# def add_product_to_cart(product_id, quantity):

#     # Check if the product exists in the cart.
#     if product_id in cart:
#         # If the product exists, increment the quantity.
#         cart[product_id]['quantity'] += quantity
#     else:
#         # If the product does not exist, add it to the cart.
#         cart[product_id] = {'quantity': quantity}

# def view_cart():

#     # Print the contents of the cart.
#     for product_id, product in cart.items():
#         print(f"{product['quantity']}x {product_id}")

# def remove_product_from_cart(product_id):

#     # Check if the product exists in the cart.
#     if product_id in cart:
#         # If the product exists, remove it from the cart.
#         del cart[product_id]



# def get_total_price(cart):
#   total_price = 0
#   for product_id, product in cart.items():
#     total_price += product['quantity'] * product['price']
#   return total_price












# # increasing and decreasing items 
# @login_required(login_url='signin')
# def increase_cart_item(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = request.user.cart
#     cart_item,  = CartItem.objects.get_or_create(cart=cart, product=product)

#     cart_item.quantity += 1
#     cart_item.save()

#     return render(request, 'invoicing.html', {'product_id':product_id})

# @login_required(login_url='signin')
# def decrease_cart_item(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = request.user.cart
#     cart_item = cart.cartitem_set.get(product=product)

#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()

#     return render(request, 'invoicing.html',  {'product_id':product_id})




# #adds products to cart
# # @login_required(login_url='signin')
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     cart = request.session.get('cart-item', Cart())
#     cart.add(product)
#     request.session['cart-item'] = cart
#     return redirect('polls:home')



# #view products in cart
# @login_required(login_url='signin')
# def view_cart(request):
#     cart = request.user.cart
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = sum(item.quantity * item.product.price for item in cart_items)
#     return render(request, 'invoicing.html', {'cart_items': cart_items, 'total_price':total_price})

# #removes products from cart
# @login_required(login_url='signin')
# def remove_from_cart(request, product_id):
#     product = Product.objects.get(pk=product_id)
#     cart = Cart.objects.get(user=request.user)
  
#     if product_id in cart:
#         del cart[product_id]
#     return render(request, 'invoicing.html' , {'product_id':product_id})
