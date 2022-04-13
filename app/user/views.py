from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from .forms import RegisterForm
from .models import NomalUser
# from carts.views import _cart_id
# from carts.models import Cart, CartItem

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
                                                last_name=last_name, 
                                                email=email, 
                                                username=username, 
                                                password=password,
                                                is_active=True)
            user.phone_number = phone_number
            user.save()

            return redirect('register')
        else:
            messages.error(request, "Register failed!")
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
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


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('login')


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'user/dashboard.html')
