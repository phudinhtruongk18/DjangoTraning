from django.shortcuts import render
from .models import Product,Photo
from comment.models import Comment
from hitcount.views import HitCountDetailView
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from category.models import Category
from .models import ProductInCategory

from django.db import IntegrityError

# <---------------------- PRODUCT VIEW ---------------------->
class ProductDetailView(HitCountDetailView):
    model = Product
    count_hit = True    
    template = 'product/product_detail.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        product = context['product']
        # get all photo for product
        photos = Photo.objects.all().filter(product=product)
        # get all comments for product
        comments = Comment.objects.all().filter(product=product)
        context.update({
            'comments': comments,
            'product': product,
            'photos': photos,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template , context=context)


@login_required(login_url='login')
def add_product(request):
    user = request.user

    # get all Category
    categories = Category.objects.all()

    # request.POST.getlist('services')
    # check services is in request or not
    # print services if services in request

    if request.method == 'POST':
        data = request.POST
        # print services
        images = request.FILES.getlist('images')

        if data['product_new'] != '':
            try:
                product, _ = Product.objects.get_or_create(
                    user=user,
                    name=data['product_new']
                )
            except IntegrityError as e:
                messages.warning(request, "Product name is exist!")
                return redirect('add_product')
        else:
            product = None

        categories = data.getlist('categories')
        # add product to all Categories
        for category in categories:
           ProductInCategory.objects.get_or_create(
                product=product,
                category_id=category
            )

        for image in images:
            photo = Photo.objects.create(
                product=product,
                image=image,
            )
        messages.info(request, "Create product success!")

        return redirect('add_product')

    context = {"categories":categories}
    return render(request, 'product/add_product.html', context)

@login_required(login_url='login')
def edit_product(request,product_id):
    user = request.user

    # check if product is created by user
    try:
        product = Product.objects.get(id=product_id, user=user)
    except Product.DoesNotExist:
        messages.warning(request, "You have no permission!")
        return render(request, 'product/edit_product.html')

    # get all Categories
    categories = Category.objects.all()

    if request.method == 'GET':
        photos = Photo.objects.all().filter(product=product)
        products_in_category = ProductInCategory.objects.all().filter(product=product)
        categories_of_product = [product_in_category.category for product_in_category in products_in_category]
        # get all images for product

        context = {
            'categories':categories,
            'product':product,
            'photos':photos,
            'categories_of_product':categories_of_product,
        }

        return render(request, 'product/edit_product.html', context)
    elif request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        # print images
        # print data
        # print data['product_new']
        if data['product_new'] != '':
            name=data['product_new']
            product.name = name
            try:
                product.save()
            except IntegrityError as e:
                messages.warning(request, "Product name is exist!")
                return redirect('edit_product', product_id)

        categories_id = data.getlist('categories')
        old_categories = ProductInCategory.objects.all().filter(product=product)
        # get category that category_id not in categories then delete
        for old_category in old_categories:
            if old_category.category.id not in categories_id:
                old_category.delete()
            else:
                categories.remove(old_category.category.id)

        # add product to new categories
        for category in categories_id:
            product_in_category, created = ProductInCategory.objects.get_or_create(
                product_id=product.id,
                category_id=category
            )

        for image in images:
            photo = Photo.objects.create(
                product=product,
                image=image,
            )

        messages.info(request, "Update product success!")
        return redirect('edit_product', product_id=product_id)

# delete product if product is created by user
@login_required(login_url='login')
def delete_product(request, product_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        product_id = int(product_id)
        product = Product.objects.get(id = product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist!")
        return redirect(url)

    if product.user.id == request.user.id:
        product.delete()
        messages.success(request, "Your product has been deleted!")
        return redirect(url)
    
    messages.error(request, "Delete product false!")
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

    if photo.product.user.id == request.user.id:
        photo.delete()
        messages.success(request, "Your photo has been deleted!")
        return redirect(url)
    
    messages.warning(request, "Delete photo false!")
    return redirect(url)
# <---------------------- /PHOTO VIEW ---------------------->
