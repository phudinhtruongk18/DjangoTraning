from django.shortcuts import render
from .models import Product,Photo
from comment.models import Comment
from hitcount.views import HitCountDetailView
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from catalog.models import Catalog
from .models import ProductInCatalog


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

    # get all catalogs
    catalogs = Catalog.objects.all()

    # request.POST.getlist('services')
    # check services is in request or not
    # print services if services in request

    if request.method == 'POST':
        data = request.POST
        # print services
        images = request.FILES.getlist('images')

        if data['product_new'] != '':
            try:
                product, created = Product.objects.get_or_create(
                    user=user,
                    name=data['product_new']
                )
            except IntegrityError as e:
                messages.warning(request, "Product name is exist!")
                return redirect('add_product')
        else:
            product = None

        catalogs = data.getlist('catalogs')
        # add product to all catalogs
        for catalog in catalogs:
            product_in_catalog, created = ProductInCatalog.objects.get_or_create(
                product=product,
                catalog_id=catalog
            )

        for image in images:
            photo = Photo.objects.create(
                product=product,
                image=image,
            )
        messages.info(request, "Create product success!")

        return redirect('add_product')

    context = {"catalogs":catalogs}
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

    # get all catalogs
    catalogs = Catalog.objects.all()
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.warning(request, "Product does not exist!")
        return render(request, 'product/edit_product.html')

    if request.method == 'GET':
        photos = Photo.objects.all().filter(product=product)
        product_in_catalog = ProductInCatalog.objects.all().filter(product=product)
        catalogs_of_product = [product_in_catalog.catalog for product_in_catalog in product_in_catalog]
        # get all images for product

        context = {
            'catalogs':catalogs,
            'product':product,
            'photos':photos,
            'catalogs_of_product':catalogs_of_product,
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
            print("name: ", name)
            product.name = name
            product.save()

        catalogs = data.getlist('catalogs')

        old_catalogs = ProductInCatalog.objects.all().filter(product=product)
        # get catalog that catalog_id not in catalogs then delete
        for old_catalog in old_catalogs:
            if old_catalog.catalog.id not in catalogs:
                old_catalog.delete()
            else:
                catalogs.remove(old_catalog.catalog.id)

        # add product to new catalogs
        for catalog in catalogs:
            product_in_catalog, created = ProductInCatalog.objects.get_or_create(
                product=product,
                catalog_id=catalog
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
        photo_id = int(photo_id)
        photo = Photo.objects.get(id = photo_id)
    except Photo.DoesNotExist:
        messages.error(request, "Photo does not exist!")
        return redirect(url)

    if photo.product.user.id == request.user.id:
        photo.delete()
        messages.success(request, "Your photo has been deleted!")
        return redirect(url)
    
    messages.error(request, "Delete photo false!")
    return redirect(url)
# <---------------------- /PHOTO VIEW ---------------------->
