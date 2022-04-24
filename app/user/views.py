from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from .forms import RegisterForm
from .models import NomalUser

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = NomalUser.objects.create_user(first_name=first_name,
                                                last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, "Confirm your email address to complete the registration")
            return redirect('register')
        else:
            messages.error(request, "Register failed!")
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'user/register.html', context=context)


def login(request):
    # check login gooogle
    if request.user.is_authenticated:
        print(request.user)
        messages.success(request, "Login successful",request.user.username,request.user.is_active)
        return redirect('dashboard')
        
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request=request, user=user)
            messages.success(request, "Login successful")

            url = request.META.get('HTTP_REFERER')
            try:
                query = request.utils.urlparse(url).query
                params = dict(x.split("x") for x in query.split("&"))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except Exception:
                return redirect('dashboard')
        else:
            messages.error(request, "Login failed!")
            messages.error(request, "Make sure that your Aram Account is activated !")
    context = {
        'email': email if 'email' in locals() else '',
        'password ': password if 'password' in locals() else '',
    }
    return render(request, 'user/login.html', context=context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = NomalUser.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated, please login!")
        return render(request, 'user/login.html')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('register')


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('login')


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'user/dashboard.html')

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import MyUserSerializer
from rest_framework import status

class MyApiRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""USER VIEW BUT NEED CATALOG AND PRODUCT"""
from category.models import Category
from product.models import Product

# Create your views here.
@login_required(login_url='login')
def user_manage_view(request):
    user = request.user
    # get all catalogs create by user
    categories = Category.objects.all().filter(user=user)
    # get all prodcut created by user
    products = Product.objects.all().filter(user=user)
    photos = [product.thumb for product in products]
    # zip 
    product_with_thumb = zip(products, photos)
    context = {'categories':categories, 'product_with_thumb':product_with_thumb}
    return render(request, 'user/user_manage_view.html', context)
