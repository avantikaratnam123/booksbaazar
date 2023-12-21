from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib import messages
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def search_query(request):
  if request.method == "GET":
    query=request.GET["q"]
    # mylist=[query]
    if query:
      
     product=Product.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
     if query not in product:
       messages.error(request,"NO RESULT FOUND!!!")
       return redirect('/')
    else:
     product=Product.objects.all()
    return render (request,'app/searched.html',{'product':product})

def home(request):
 return render(request, 'app/home.html')

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

@login_required
def add_to_cart(request):
 user = request.user
 product_id=request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form = CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,'congratulations!! profile updated successfully')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
@login_required
def address(request):
  add = Customer.objects.filter(user=request.user)
  return render(request,'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

# def mobile(request):
#  return render(request, 'app/mobile.html')

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')

class ProductView(View):
 def get(self,request):
  spiritual = Product.objects.filter(category='S')
  yoga = Product.objects.filter(category='Y')
  diet = Product.objects.filter(category='D')
  astrology = Product.objects.filter(category='AS')
  return render(request,'app/home.html',{'spiritual':spiritual,'yoga':yoga,'diet':diet,'astrology':astrology})
 
class ProductDetailView(View):
  def get(self,request,pk):               
    product = Product.objects.get(pk=pk)
    share_link = request.build_absolute_uri(reverse('product-detail', args=[pk]))
    item_already_in_cart = False
    if request.user.is_authenticated:
       item_already_in_cart=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
    return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'share_link':share_link})
      

class CustomerRegistrationView(View):
  def get(self,request):
     form= CustomerRegistrationForm()
     return render(request,'app/customerregistration.html',{'form':form})
  def post(self,request):
    form = CustomerRegistrationForm(request.POST)
    if form .is_valid():
      messages.success(request,'congratulations!!! Registered successfully')
      form.save()
    return render(request,'app/customerregistration.html',{'form':form})
  
@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all()if p.user == user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity*p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
    else:
      return render(request,'app/emptycart.html')
    



    
def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q (product=prod_id)& Q(user=request.user))
    c.quantity += 1
    c.save()
    amount =0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity* p.product.discounted_price)
      amount += tempamount
      
    data = {
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount
    }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q (product=prod_id)& Q(user=request.user))
    c.quantity -= 1
    c.save()
    amount =0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity* p.product.discounted_price)
      amount += tempamount
       
    data = {
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':amount+shipping_amount
    }
    return JsonResponse(data) 
  
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q (product=prod_id)& Q(user=request.user))
    c.delete()
    amount =0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity* p.product.discounted_price)
      amount += tempamount
      
    data = {
    
      'amount':amount,
      'totalamount':amount+shipping_amount
    }
    return JsonResponse(data) 
  






@login_required 
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount   =  0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
   for p in cart_product:
       tempamount = (p.quantity * p.product.discounted_price)
       amount += tempamount
   totalamount = amount+shipping_amount

 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

@login_required
def orders(request):
   op = OrderPlaced.objects.filter(user=request.user)
   return render(request,'app/orders.html',{'order_placed':op})

def spiritualbooks(request,data=None):
  if data == None:
    sbooks = Product.objects.filter(category = 'S')
  elif data =='below':
    sbooks = Product.objects.filter(category='S').filter(discounted_price__lt =300)
  elif data =='above':
    sbooks = Product.objects.filter(category='S').filter(discounted_price__gt =300)
  return render(request, 'app/spiritualbooks.html',{'sbooks':sbooks})

def yogabooks(request,data=None):
  if data == None:
    ybooks = Product.objects.filter(category = 'Y')
  elif data =='below':
    ybooks = Product.objects.filter(category='Y').filter(discounted_price__lt =300)
  elif data =='above':
    ybooks = Product.objects.filter(category='Y').filter(discounted_price__gt =300)
  return render(request, 'app/yogabooks.html',{'ybooks':ybooks})

def dietbooks(request,data=None):
  if data == None:
    dbooks = Product.objects.filter(category = 'D')
  elif data =='below':
    dbooks = Product.objects.filter(category='D').filter(discounted_price__lt =300)
  elif data =='above':
    dbooks = Product.objects.filter(category='D').filter(discounted_price__gt =300)
  return render(request, 'app/dietbooks.html',{'dbooks':dbooks})

def astrologybooks(request,data=None):
  if data == None:
    asbooks = Product.objects.filter(category = 'AS')
  elif data =='below':
    asbooks = Product.objects.filter(category='AS').filter(discounted_price__lt =300)
  elif data =='above':
    asbooks = Product.objects.filter(category='AS').filter(discounted_price__gt =300)
  return render(request, 'app/astrologybooks.html',{'asbooks':asbooks})

# def share_product(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     share_link = request.build_absolute_uri(reverse( ProductDetailView, args=[product_id]))
    