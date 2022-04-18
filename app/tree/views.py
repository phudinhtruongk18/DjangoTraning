from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.contrib import messages

from .models import Catalog, ProductInCatalog, Product, Photo,Comment
from .forms import CommentForm

from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView

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
        print(comments)
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

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = Comment.objects.get(user__id=request.user.id, product__id=product_id)
            form = CommentForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thanks for the updating review!")
            return redirect(url)
        except Exception as e:
            print(e)
            form = CommentForm(request.POST)
            if form.is_valid():
                data = Comment()
                data.review = form.cleaned_data['content']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thanks for the review!")
                return redirect(url)