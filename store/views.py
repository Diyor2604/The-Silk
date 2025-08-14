from django.shortcuts import render,redirect
from .models import Items,Category,Profile 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    #Determine if they filled out the form 
    if request.method == "POST":
        searched=request.POST['searched']
        #Query  The Products DB  Model 
        searched=Items.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #Test for null
        if not searched:
           messages.success(request,"That product does nit exist....Please try again")   
           return render(request,'store/search.html',{})
        else:
           return render(request,'store/search.html',{'searched':searched})  
    else:
        return render(request,'store/search.html',{})




def update_info(request):
     if request.user.is_authenticated:
         #Get current user
         current_user=Profile.objects.get(user__id=request.user.id)
         #Get current UsersShippingInfo
         shipping_user=ShippingAddress.objects.get(id=request.user.id)

         #Get the original user Form
         form=UserInfoForm(request.POST or None,instance=current_user)
         #get users shipping form
         shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
         if form.is_valid() or shipping_form.is_valid():
             #SAve original Form
             form.save()
             #Save Shipping Form
             shipping_form.save()
             messages.success(request,"Your Info has been updated")
             return redirect('home')
         return render(request,'store/update_info.html',{'form':form,'shipping_form':shipping_form})
     else:
         messages.error(request,"You must be logged in to access that page")
         return redirect('home')  



def update_password(request):
     if request.user.is_authenticated:
          current_user=request.user
          #Did they fill oput the form
          if request.method == 'POST':
             forms=ChangePasswordForm(current_user,request.POST)
             #Is the Form Valid
             if form.is_valid():
                 form.save()
                 messages.success(request,"Your PAssword has been updated ,Please Login again.....")
                 #login(request,current_user)
                 return redirect('home')
             else:
                 for error in list(form.errors.values()):
                   messages.error(request,error)
                   return redirect('store/update_passwordd')
          else:
              form=ChangePasswordForm(current_user)
              return redirect(request,'store/update_password.html',{})
     else:
          messages.success(request,"You must be logged in to View that page")
          return redirect('home')


def update_user(request):
     if request.user.is_authenticated:
         current_user=User.objects.get(id=request.user.id)
         user_form=UpdateUserForm(request.POST or None,instance=current_user)

         if user_form.is_valid():
             user_form.save()


             login(request,current_user)
             messages.success(request,"User has been updated")
             return redirect('home')
         return render(request,'store/update.html',{'user_form':user_form})
     else:
         messages.success(request,"You must be logged in to access that page")
         return redirect('home')

     


def category_summary(request):
     categories=Category.objects.all()
     return render(request,'store/category_summary.html',{"categories":categories})


# Create your views here.
def category(request,foo):
    foo=foo.replace('-',' ')
    try:
        category=Category.objects.get(name=foo)
        products=Items.objects.filter(category=category)
        return render(request,'store/category.html',{'products':products,'category':category})
    except:
        messages.success(request,("That Category does not exist"))
        return redirect('home')

def product(request,pk):
    product=Items.objects.get(id=pk)
    return render(request,'store/product.html',{'product':product})


def home(request):
     items=Items.objects.all()
     return render(request, 'store/home.html', {'product':items})

def about(request):
     return render(request, 'store/about.html', {})


def log_in_user(request):
     if request.method == "POST":
          username=request.POST['username']
          password=request.POST['password']
          user=authenticate(request,username=username, password=password)
          if user is not None:
               login(request,user)
               #Do some shoping cart stuff

               current_user=Profile.objects.get_or_create(user__id=request.user.id)
               # Get their saved cart from database
               saved_cart=current_user.old_cart
               #convert database string to python dictionary
               if saved_cart:
                   #Convert to dictionary using JSON
                   converted_cart=json.loads(saved_cart)
                   #Add the cart dictionary to our cart session
                   #Get the cart
                   cart=Cart(request)
                   #Loop the through the cart and add the items from the database
                   for key,value in converted_cart.items():
                       cart.db_add(product=key,quantity=value)
                       







               messages.success(request,("You Have been logged in !"))
               return redirect('home')
          else:
               messages.success(request,("There was error ,Please try again!"))
               return redirect('login') 
     else:


      return render(request, 'store/Log_in.html', {})

def log_out_user(request):
     logout(request)
     messages.success(request,("You have been logged out !"))
     return redirect('home')
    
def register_user(request):    
     form=SignUpForm()
     if request.method=="POST":
          form=SignUpForm(request.POST)
          if form.is_valid():
               form.save()
               username=form.cleaned_data['username']
               password=form.cleaned_data['password1'] 
               #log in user
               user=authenticate(username=username,password=password)
               login(request,user)   
               messages.success(request,("Username Created - Please Fill Out Your User Info Below ....!")) 
               return redirect('update_user')
          else:
               messages.success(request,("Please,try again......!")) 
               return redirect('register')
     else:
      return render(request, 'store/register.html', {'form':form})