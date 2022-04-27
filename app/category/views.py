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

from product.models import ProductInCategory

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# Display Posts
from rest_framework.decorators import api_view

from django.db import IntegrityError

from .models import Category
# from .forms import CategoryForm
from .serializers import CategorySerializer
from .my_exception import MyValidationError

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
    
class CategoryList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    class Meta:
        read_only_fields = ('name', 'slug',)


class CategoryDetail(generics.RetrieveAPIView):

    serializer_class = CategorySerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Category, slug=item)

# Category Search


class CategoryListDetailfilter(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ['^slug']

# Post Admin

# class CreatePost(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class CreateCategory(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCategoryDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EditCategory(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class DeleteCategory(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class CategoryListView(ListView):
    model = Category
    # comment this line to see all categories (without pagination)
    paginate_by = 3
    context_object_name = 'paged_categories'
    template_name = 'category/categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        all_categories = Category.objects.all()
        all_categories_count = all_categories.count()
        # print('context->',context)

        context.update({
            'categories_count': all_categories_count,
            'all_categories': all_categories,
        })

        return context

class CategoryDetailView(HitCountDetailView):
    model = Category
    count_hit = True    
    template = 'category/products_by_category.html'
    
    slug_field = 'slug'

    def get_context_data(self,page, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # check attribute of object
        # print('context->',context)

        category = context['category']
        products = ProductInCategory.objects.all().filter(category=category)

        panigator = Paginator(products, 3)
        paged_products = panigator.get_page(page)
        products_count = products.count()

        context.update({
            'category': category if 'category' in locals() else None,
            'paged_products': paged_products,
            'products_count': products_count,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        page = request.GET.get('page')
        page = page or 1
        context = self.get_context_data(page=page,object=self.object)
        return render(request, 'category/products_by_category.html', context=context)

# def products_by_category(request, category_slug=None):

#     if category_slug is not None:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = ProductInCategory.objects.all().filter(category=category)
#     else:
#         products = ProductInCategory.objects.all().filter().order_by('product')

#     page = request.GET.get('page')
#     page = page or 1
#     panigator = Paginator(products, 3)
#     paged_products = panigator.get_page(page)
#     products_count = products.count()

#     context = {
#         'category': category if 'category' in locals() else None,
#         'paged_products': paged_products,
#         'products_count': products_count,
#    }
#     return render(request, 'category/products_by_category.html', context=context)

# create Category with image(optional) if user is login
@login_required(login_url='login')
def add_category(request):
    # get Categorys to get parent Category 
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        name = data['category_new']
        parent_category_id = data.get('parent_category')
        # get parent Category
        parent_category = None
        if parent_category_id != 'none':
            try:
                parent_category = Category.objects.get(id=int(parent_category_id))
            except Category.DoesNotExist:
                messages.warning(request, "Parent Category does not exist!")
                return render(request, 'category/add_category.html', {'categories':categories})
            
        try:
            category = Category.objects.create(
            parent=parent_category,
            name=name,
            user=request.user,
            image = image
            )
            category.save()
        except IntegrityError:
            messages.warning(request, "This category is already exist! Pick another name!")
            return render(request, 'category/add_category.html', {'categories':categories})

        messages.info(request, "Create Category success!")
        return redirect('category:add_category')
    
    context = {
        'categories':categories,
    }
    return render(request, 'category/add_category.html', context)

# delete Category if user is login
@login_required(login_url='login')
def delete_category(request, category_id):
    url = request.META.get('HTTP_REFERER')
    # check login and check user
    try:
        category_id = int(category_id)
        category = Category.objects.get(id = category_id)
    except Category.DoesNotExist:
        messages.warning(request, "Category does not exist!")
        return redirect(url)

    if category.user.id == request.user.id:
        category.delete()
        messages.success(request, "Your category has been deleted!")
        return redirect(url)
    
    messages.warning(request, "Delete category false!")
    return redirect(url)

# edit Category if user is login
@login_required(login_url='login')
def edit_category(request, category_id):
    # check login and check user
    # form = CategoryForm()
    try:
        category_id = int(category_id)
        category = Category.objects.get(id = category_id)
    except Category.DoesNotExist:
        messages.warning(request, "Category does not exist!")
        return redirect('category:edit_category')

    categories = Category.objects.all()

    if category.user.id == request.user.id:
        if request.method == 'GET':
            context = {
                'category':category,
                'categories':categories,
                # 'form':form,
            }
            return render(request, 'category/edit_category.html', context)
        elif request.method == 'POST':
            data = request.POST
            image = request.FILES.get('image')
            name = data['category_new']
            parent_category = data.get('parent_category')
            # get parent Category
            try:
                parent_category = Category.objects.get(id=int(parent_category))
            except Category.DoesNotExist:
                messages.warning(request, "Parent Category does not exist!")
                return render(request, 'category/edit_category.html', {'category':category})
            
            category.name = name
            category.parent = parent_category
            if image:
                category.image = image

            try:
                category.save()
            except IntegrityError:
                messages.warning(request, "Pick another name!")
                return redirect('category:edit_category')
            except MyValidationError as e:
                messages.warning(request, str(e))
                return redirect('category:edit_category')


            messages.info(request, "Update Category success!")
            return redirect('category:edit_category', category_id=category_id)
    messages.warning(request, "Update Category false!")
    return redirect('category:edit_category')

