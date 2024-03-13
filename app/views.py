from typing import Any

from django.shortcuts import render, redirect
from django.views import View
from .models import Cart,Customer,Product,OrderPlaced
from .forms import CustomarRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
  def get(self,request):
   topwearsmale=Product.objects.filter(category='Top Wear Male')
   topwearsfemale=Product.objects.filter(category='Top Wear Female')
   return render(request,'app/home.html',{'topwearsmale':topwearsmale,'topwearsfemale':topwearsfemale})

class ProductDetailView(View):
 def get(self,request,pk):
  item_already_in_cart = False
  item_already_in_cart = Cart.objects.filter(Q(product='product.id') & Q(user=request.user)).exists()
  product=Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',{'product': product, 'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect ('/cart')

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    print(cart)
    amount= 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    #print(cart_product)
    if cart_product:
       for p in cart_product:
          tempamount = (p.quantity * p.product.discounted_price)
          amount += tempamount
       totalamount = amount+shipping_amount
    return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
  else:
      return render(request, 'app/emptycart.html ')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
             'quantity': c.quantity,
             'amount':amount,
             'totalamount':amount + shipping_amount
         }
    return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
             'quantity': c.quantity,
             'amount':amount,
             'totalamount':amount + shipping_amount
         }
    return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
             'amount':amount,
             'totalamount':amount + shipping_amount
         }
    return JsonResponse(data)



@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html', {'order_placed':op})


def mobile(request):
 return render(request, 'app/mobile.html')


class CustomerRegistrationView(View):
 def get(self,request):
  form =CustomarRegistrationForm()
  return render(request,'app/customerregistration.html', {'form':form})

 def post(self,request):
  form=CustomarRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulation!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
  user: Any = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shiping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shiping_amount
  return render(request, "app/checkout.html", {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

@login_required
def payment_done(request):
   user = request.user
   custid = request.GET.get('custid')
   customer = Customer.objects.all(id=custid)
   cart = Cart.objects.filter(user=user)
   for c in cart:
       OrderPlaced(user=user, customer=customer, product=c, quantity=c.quantity).save()
       c.delete()
   return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self,request):
    form =CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form, 'active':'btn-primary'})

def post(self,request):
  form= CustomerProfileForm(request.POST)
  if form.is_valid():
   user=request.user
   name = form.cleaned_date['name']
   locality = form.cleaned_date['locality']
   city = form.cleaned_date['city']
   state = form.cleaned_date['state']
   zipcode = form.cleaned_date['zipcode']
   reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulations! Profile Update Successfully ')
  return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})