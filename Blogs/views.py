from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import TemplateView # Import TemplateView
from django.contrib.auth.forms import UserCreationForm
from polls.models import Product,CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from polls.forms import Rating
from tasks.forms import TaskForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum







def your_invoice(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=invoice.txt'

    try:
        cart_items = CartItem.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponse('Error: Cart does not exist for this user.')

    cart_subtotal = cart_items.aggregate(Sum('total_price'))
    cart_total = cart_subtotal['total_price__sum']

    inside = [f'{cart_item.product}\n{cart_item.quantity} x ${cart_item.product.price} = ${cart_item.total_price}\n' for cart_item in cart_items]
    inside.append(f'\nSubtotal: ${cart_subtotal["total_price__sum"]}\n')
    inside.append(f'Tax: $0\n')
    inside.append(f'Total: ${cart_total}\n')

    response.writelines(inside)
    return response



# Payment module
@login_required(login_url='polls:signin')
def Pay_here(request):
    user =request.user
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            usertask= form.save(commit=False)
            usertask.taskedby=user
            form.save()
            # order.ordered_by= user
            messages.success(request, "Your delivery information submitted succesfully, kindly proceed to payment")
            return redirect('Blogs:checkout')
    else:
        form=TaskForm()
    
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    return render(request,'checkout.html' ,{'form':form , 'total_price':total_price})


# Create your views here.
def Reviews(request):
    form = UserCreationForm
    return render(request,"blogs.html", {'form':form})


def Aboutus(request):
    return render(request,'about-us.html')

