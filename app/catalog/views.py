""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from product.models import ProductInCatalog

from django.shortcuts import get_object_or_404
from .models import Catalog
from .serializers import CatalogSerializer
from rest_framework import viewsets, filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# Display Posts
from rest_framework.decorators import api_view

@api_view(['GET'])
def catalog_list(request):
    catalogs = Catalog.objects.all()
    serializer = CatalogSerializer(catalogs, many=True)
    return Response(serializer.data)
    
class CatalogList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()
    class Meta:
        read_only_fields = ('name', 'slug',)


class CatalogDetail(generics.RetrieveAPIView):

    serializer_class = CatalogSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Catalog, slug=item)

# Catalog Search


class CatalogListDetailfilter(generics.ListAPIView):

    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ['^slug']

# Post Admin

# class CreatePost(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class CreateCatalog(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCatalogDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class EditCatalog(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()


class DeleteCatalog(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.all()



class CatalogListView(ListView):
    model = Catalog
    context_object_name = 'catalog'
    template_name = 'catalog/catalogs.html'

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

class CatalogDetailView(HitCountDetailView):
    model = Catalog
    count_hit = True    
    template = 'catalog/products_by_catalog.html'
    slug_field = 'slug'

    def get_context_data(self,page, **kwargs):
        context = super(CatalogDetailView, self).get_context_data(**kwargs)

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
        return render(request, 'catalog/products_by_catalog.html', context=context)

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
    return render(request, 'catalog/products_by_catalog.html', context=context)

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
            return render(request, 'catalog/add_catalog.html', {'catalogs':catalogs})
            
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
    return render(request, 'catalog/add_catalog.html', context)

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
            return render(request, 'catalog/edit_catalog.html', context)
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
                return render(request, 'catalog/edit_catalog.html', {'catalog':catalog})
            
            catalog.name = name
            catalog.parent = parent_catalog
            if image:
                catalog.image = image
            catalog.save()
            messages.info(request, "Update catalog success!")
            return redirect('edit_catalog', catalog_id=catalog_id)
    messages.error(request, "Update catalog false!")
    return redirect(url)
