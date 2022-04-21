from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib import messages

from .models import Catalog, ProductInCatalog, Product, Photo,Comment
from .forms import CommentForm

from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView
from django.contrib.auth.decorators import login_required

class CatalogListView(ListView):
    model = Catalog
    context_object_name = 'catalog'
    template_name = 'tree/catalogs.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        
        all_catalog = Catalog.objects.all()
        
        page = self.request.GET.get('page')
        page = page or 1

        panigator = Paginator(all_catalog, 6)
        paged_catalog = panigator.get_page(page)
        all_catalog_count = all_catalog.count()

        context = {
            'paged_catalog': paged_catalog,
            'catalogs_count': all_catalog_count,
            'all_catalog': all_catalog,
        }

        return context


class CategoryDetailView(HitCountDetailView):
    model = Catalog
    count_hit = True    
    template = 'tree/products_by_catalog.html'
    slug_field = 'slug'

    def get_context_data(self,page, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        catalog = context['catalog']
        products = ProductInCatalog.objects.all().filter(catalog=catalog)

        panigator = Paginator(products, 3)
        paged_products = panigator.get_page(page)
        products_count = products.count()

        context.update({
            'catalog': catalog if 'catalog' in locals() else None,
            'paged_products': paged_products,
            'products_count': products_count,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        page = request.GET.get('page')
        page = page or 1
        context = self.get_context_data(page=page,object=self.object)
        return render(request, 'tree/products_by_catalog.html', context=context)

def products_by_catalog(request, catalog_slug=None):

    if catalog_slug is not None:
        catalog = get_object_or_404(Catalog, slug=catalog_slug)
        products = ProductInCatalog.objects.all().filter(catalog=catalog)
    else:
        products = ProductInCatalog.objects.all().filter().order_by('product')

    page = request.GET.get('page')
    page = page or 1
    panigator = Paginator(products, 3)
    paged_products = panigator.get_page(page)
    products_count = products.count()

    context = {
        'catalog': catalog if 'catalog' in locals() else None,
        'paged_products': paged_products,
        'products_count': products_count,
   }
    return render(request, 'tree/products_by_catalog.html', context=context)


class ProductDetailView(HitCountDetailView):
    model = Product
    count_hit = True    
    template = 'tree/product_detail.html'
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
def delete_comment(request, comment_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        comment_id = int(comment_id)
        comment = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist:
        messages.error(request, "comment does not exist!")
        return redirect(url)

    if comment.user.id == request.user.id:
        comment.delete()
        messages.success(request, "Your review has been deleted!")
        return redirect(url)
    
    messages.error(request, "Delete comment false!")
    return redirect(url)

@login_required(login_url='login')
def submit_comment(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(user__id=request.user.id, product__id=product_id)
            form = CommentForm(request.POST, instance=comment)
            form.save()
            messages.success(request, "Thanks for the updating review!")
            return redirect(url)
        except Exception as e:
            print(e)
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.content = form.cleaned_data['content']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thanks for the review!")
                return redirect(url)

from django.db.utils import IntegrityError

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
    return render(request, 'tree/add_product.html', context)

@login_required(login_url='login')
def user_manage_view(request):
    user = request.user
    # get all catalogs create by user
    catalogs = Catalog.objects.all().filter(user=user)
    # get all prodcut created by user
    products = Product.objects.all().filter(user=user)
    photos = [product.thumb for product in products]
    # zip 
    product_with_thumb = zip(products, photos)
    context = {'catalogs':catalogs, 'product_with_thumb':product_with_thumb}
    return render(request, 'tree/user_manage_view.html', context)

@login_required(login_url='login')
def edit_product(request,product_id):
    user = request.user

    # check if product is created by user
    try:
        product = Product.objects.get(id=product_id, user=user)
    except Product.DoesNotExist:
        messages.warning(request, "You have no permission!")
        return render(request, 'tree/edit_product.html')

    # get all catalogs
    catalogs = Catalog.objects.all()
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.warning(request, "Product does not exist!")
        return render(request, 'tree/edit_product.html')

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

        return render(request, 'tree/edit_product.html', context)
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

# add photo in product
# @login_required(login_url='login')
# def add_photo(request, product_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             product = Product.objects.get(id=product_id)

#             if product.user.id == request.user.id:
#                 image = request.FILES['image']
#                 photo = Photo.objects.create(
#                     product=product,
#                     image=image,
#                 )
#                 messages.success(request, "Add photo success!")
#                 return redirect(url)
#         except Exception as e:
#             print(e)
#             messages.error(request, "Add photo false!")
#             return redirect(url)
#     messages.error(request, "Add photo false!")
#     return redirect(url)

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

# create catalog with image(optional) if user is login
@login_required(login_url='login')
def add_catalog(request):
    # get catalogs to get parent catalog 
    catalogs = Catalog.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        name = data['catalog_new']
        parent_catalog = data.get('parent_catalog')
        # get parent catalog
        try:
            parent_catalog = Catalog.objects.get(id=int(parent_catalog))
        except Catalog.DoesNotExist:
            messages.error(request, "Parent catalog does not exist!")
            return render(request, 'tree/add_catalog.html', {'catalogs':catalogs})
            
        user = request.user
        catalog = Catalog.objects.create(
            parent=parent_catalog,
            name=name,
            user=user,
            image = image
        )
        catalog.save()
        messages.info(request, "Create catalog success!")
        return redirect('add_catalog')
    
    context = {
        'catalogs':catalogs,
    }
    return render(request, 'tree/add_catalog.html', context)

# delete catalog if user is login
@login_required(login_url='login')
def delete_catalog(request, catalog_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        catalog_id = int(catalog_id)
        catalog = Catalog.objects.get(id = catalog_id)
    except Catalog.DoesNotExist:
        messages.error(request, "Catalog does not exist!")
        return redirect(url)

    if catalog.user.id == request.user.id:
        catalog.delete()
        messages.success(request, "Your catalog has been deleted!")
        return redirect(url)
    
    messages.error(request, "Delete catalog false!")
    return redirect(url)

# edit catalog if user is login
@login_required(login_url='login')
def edit_catalog(request, catalog_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        catalog_id = int(catalog_id)
        catalog = Catalog.objects.get(id = catalog_id)
    except Catalog.DoesNotExist:
        messages.error(request, "Catalog does not exist!")
        return redirect(url)

    catalogs = Catalog.objects.all()

    if catalog.user.id == request.user.id:
        if request.method == 'GET':
            context = {
                'catalog':catalog,
                'catalogs':catalogs,
            }
            return render(request, 'tree/edit_catalog.html', context)
        elif request.method == 'POST':
            data = request.POST
            image = request.FILES.get('image')
            name = data['catalog_new']
            parent_catalog = data.get('parent_catalog')
            # get parent catalog
            try:
                parent_catalog = Catalog.objects.get(id=int(parent_catalog))
            except Catalog.DoesNotExist:
                messages.error(request, "Parent catalog does not exist!")
                return render(request, 'tree/edit_catalog.html', {'catalog':catalog})
            
            catalog.name = name
            catalog.parent = parent_catalog
            if image:
                catalog.image = image
            catalog.save()
            messages.info(request, "Update catalog success!")
            return redirect('edit_catalog', catalog_id=catalog_id)
    messages.error(request, "Update catalog false!")
    return redirect(url)
