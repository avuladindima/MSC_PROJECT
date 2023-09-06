from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from .models import Drug,Doctor,Prescription,Patient,prescriptionDrugs,drug_choices 
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from .forms import PrescriptionForm
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,user_logged_in,user_logged_out,authenticate
from django.urls import reverse
from django.conf import settings
from .cart_update import CartUpdate



# Create your views here.

def index(request):
    return render(request,'index.html')

class shopView(generic.ListView):
    
    context_object_name = "list_of_drugs"
    
    template_name = 'shop.html'
    
    def get_queryset(self):
        return Drug.objects.order_by('name')
    
    #return render(request,'shop.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def cart(request):
    return render(request,'cart.html')

def thankyou(request):
    return render(request,'thankyou.html')

def login_(request):
    #error_message = None
    if request.method == 'POST':
        username = request.POST.get('c_email')
        password = request.POST.get('c_password')
        print(f'username: {username} password:{password}')
        user = authenticate(username=username, password=password)
        
        print(user)
        if user is not None:
            login(request,user)  # Log the user in
            return redirect('shop')  # Redirect to the home page or any other page
        else:
            # Authentication failed, show an error message
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')
 

def signup(request):
    if request.method =="POST":
        name = f"{request.POST.get('c_fname')}  {request.POST.get('c_lname')}"
        email = request.POST.get('c_email')
        phone = request.POST.get('c_phone')
        address = request.POST.get('c_address')
        country = request.POST.get('c_country')
        street = request.POST.get('c_street')
        gender = request.POST.get('c_gender')
        password = request.POST.get('c_password')
        
        user = User.objects.create_user(username=email, password=password,email=email,last_name=request.POST.get('c_lname'),first_name= request.POST.get('c_fname'))
        #user = User.objects.get(username=email)
        new_patient = Patient(name=name,gender=gender,phone=phone,address=address,street=street,country=country,user_id=user)
        new_patient.save()
        user = authenticate(username=email,password=password)
        if user is not None:
            login(request,user)  # Log the user in
            return redirect('shop')
        else: 
            return render(request,'signup.html')

    return render(request,'signup.html')

@login_required
def checkout(request):
    return render(request,'checkout.html')

def singleshop(request,drug_id):
    drug = get_object_or_404(Drug,id=drug_id)
    drug_choice = [elem[0] for elem in drug_choices]
    context = {"drug" : drug,'drug_choices':drug_choice}
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        dosage = request.POST.get('c_dosage')
        medicine_type = request.POST.get('medicine_type')
        flavour = request.POST.get('c_flavour')
        cart=CartUpdate(request)
        cart.cart_update_add(product=drug,dosage=dosage,quantity=quantity,drug_type=medicine_type,flavour=flavour)
        return redirect('shop')
    return render(request,'singleshop.html',context)

#@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    drug = Drug.objects.get(id=id)
    context = {"drug" : id}
    cart.add(drug)
    return redirect("singleshop",context)


#@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    drug = Drug.objects.get(id=id)
    cart.remove(drug)
    return redirect("cart")



def item_increment(request, id):
    cart = Cart(request)
    drug = Drug.objects.get(id=id)
    cart.add(drug)
    return redirect("cart")


#@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    drug = Drug.objects.get(id=id)
    cart.decrement(drug)
    return redirect("cart")


#@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")




@login_required
def createprescriptionView(request):
    if request.method == "POST":
        doctor = request.POST.get('c_doctor')
        patient = request.POST.get('c_patient')
        print(doctor)
        doctor_ = Doctor.objects.get(id = int(doctor))
        user = User.objects.get(email=patient)
        
        patient_ = Patient.objects.get(user_id=user)
        
        
        pres = Prescription(doctor_id=doctor_,patient_id=patient_)
        pres.save()
        pres.name = pres.computed_field
        pres.save()
        
               
        drug_ids=[value['product_id'] for value in request.session[settings.CART_SESSION_ID].values()]
        quantity=[value['quantity'] for value in request.session[settings.CART_SESSION_ID].values()]
        flavours=[value['flavour'] for value in request.session[settings.CART_SESSION_ID].values()]
        dosage=[value['dosage'] for value in request.session[settings.CART_SESSION_ID].values()]
        drug_type=[value['drug_type'] for value in request.session[settings.CART_SESSION_ID].values()]
        
        print(drug_ids)
        pres_drug = prescriptionDrugs()
        pres_drug.add_drugs(drugids=drug_ids,presid=pres,flavours=flavours,quantity=quantity,dosage=dosage,drug_type=drug_type)
        cart = Cart(request)
        cart.clear()
        return redirect('thankyou')
    
    form = PrescriptionForm()
    doctors = Doctor.objects.order_by('name')
    
    return render(request,'prescription.html',{'form': form,'doctors':doctors})
@login_required    
def log_out(request):
    logout(request)  # Log out the user
    return redirect(reverse('login'))   

