from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import *
from django.views import View
import bcrypt
from django.forms import modelformset_factory
from django.views.generic import ListView, DetailView

# render home page
def index(request):
    context={
        'products': Product.objects.all().order_by("-created"),
    }
    return render(request, "index.html", context)

#process registration and redirect
def register(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key,error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(email=request.POST['email'].lower(), password=pw_hash, first_name=request.POST['first_name'], last_name=request.POST['last_name'],birthday=request.POST['birthday'])
        request.session['user_id'] = user.id #generated by django
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        messages.success(request, "Registered successfully :)")
        return redirect("/")    

# process login info and redirect
def login(request):
    errors = User.objects.login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'].lower())
        if len(user) < 1:
            messages.error(request, "No User for that email")
            return redirect("/signin")
        
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print(f"LOG - Setting session value 'user_id' = {user[0].id}")
            request.session['user_id'] = user[0].id
            request.session['first_name'] = user[0].first_name
            return redirect("/")
        else:
            messages.error(request, "Incorrect Password!")
            return redirect("/signin")

# logout and redirect
def logout(request):
    request.session.clear()
    messages.success(request, "Log out successful!")
    print(f"LOG - Log out successful, redirecting to home")  
    return redirect("/")


# registration page
def signin(request):
    return render(request, 'signin.html')

def upload(request):
    if request.user.is_authenticated:
        return render(request, 'upload.html')
    elif 'user_id' in request.session:
        return render(request, 'upload.html')
    else:
        messages.error(request, "Login first")
        return redirect("/signin")

def create_list(request):
    if request.method == 'POST':
        print(request.FILES)
        if request.user.is_authenticated:
            user = request.user
            product = Product.objects.create(social_id = user ,name = request.POST['name'], description = request.POST['desc'], category=request.POST['category'])
        elif 'user_id' in request.session:
            user = User.objects.get(id= request.session['user_id'])
            print(request.POST['category'])
            product = Product.objects.create(user_id = user ,name = request.POST['name'], description = request.POST['desc'], category=request.POST['category'])
        for i in range(4):
            if 'image'+str(i) in request.FILES:
                pic = request.FILES['image'+str(i)]
                Images.objects.create(product_id=product, image=pic)
        return redirect('/')

def show(request, id):
    user_id = 0
    if request.user.is_authenticated:
        user_id = request.user.id
    elif 'user_id' in request.session:
        user_id = request.session['user_id']
    context={
        'product': Product.objects.get(id=id),
        'user_id': user_id
    }
    return render(request, 'show.html', context)

def about(request):
    return render(request, 'about.html')

def edit_product(request, id):
    if request.POST:
        errors = Product.objects.product_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(f'/edit/{id}')
        else:
            product = Product.objects.get(id=id)
            product.name = request.POST['name']
            product.description = request.POST['desc']
            product.category = request.POST['category']
            product.save()
            return redirect('/show/'+ str(id))
    else:
        context={
            'product':Product.objects.get(id=id)
        }
        return render(request, 'edit_product.html', context)

def delete(request, id):
    product = Product.objects.get(id=id)

    product.delete()

    return redirect('/')

def category(request, string):
    context= {
        'cat': string,
        'products': Product.objects.all().order_by("-created"),
    }
    return render(request, "category.html", context)

def shop(request):
    context={
        'products': Product.objects.all().order_by("-created"),
    }
    return render(request, 'shop.html', context)
