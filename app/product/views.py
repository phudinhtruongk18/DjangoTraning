from django.forms import ValidationError
from django.shortcuts import render

from comment.models import Comment
from hitcount.views import HitCountDetailView
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from category.models import Category

# from .models import ProductInCategory
from .forms import ProductForm
from .models import Product,Photo

from django.db import IntegrityError

# <---------------------- PRODUCT VIEW ---------------------->
class ProductDetailView(HitCountDetailView):
    model = Product
    count_hit = True
    template = 'product/product_detail.html'
    slug_field = 'slug'

@login_required(login_url='login')
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    context = {
        'type_of_crud':'Add',
        'form':form,
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.save()

                for category in form.cleaned_data['categories']:
                    product.categories.add(category)
                    
                for photo in request.FILES.getlist('photos'):
                    Photo.objects.create(image=photo,product=product)
                
                

                messages.success(request, 'Product created successfully')
            except ValidationError as e:
                messages.warning(request, e)
    return render(request, 'product/add_edit_product.html', context)

@login_required(login_url='login')
def edit_product(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    context = {
        'type_of_crud':'Edit',
        'form':form,
        'product':product,
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                product = form.save(commit=True)
                for photo in request.FILES.getlist('photos'):
                    Photo.objects.create(image=photo,product=product)

                messages.success(request, 'Product updated successfully')
            except ValidationError as e:
                messages.warning(request, e)
    return render(request, 'product/add_edit_product.html', context)

# delete product if product is created by user
@login_required(login_url='login')
def delete_product(request, product_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        product_id = int(product_id)
        product = Product.objects.get(id = product_id)
        if product.owner.id == request.user.id:
            product.delete()
            messages.success(request, "Your product has been deleted!")
            return redirect(url)
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist!")
        return redirect(url)
# <---------------------- /PRODUCT VIEW ---------------------->


# <---------------------- PHOTO VIEW ---------------------->
# delete photo in product
@login_required(login_url='login')
def delete_photo(request, photo_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        photo = Photo.objects.get(id = int(photo_id))
    except Photo.DoesNotExist:
        messages.warning(request, "Photo does not exist!")
        return redirect(url)

    if photo.product.owner.id == request.user.id:
        photo.delete()
        messages.success(request, "Your photo has been deleted!")
        return redirect(url)
    
    messages.warning(request, "Delete photo false!")
    return redirect(url)
# <---------------------- /PHOTO VIEW ---------------------->
