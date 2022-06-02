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

from django.core.exceptions import ValidationError

from .models import Category
# from .forms import CategoryForm
# from .my_exception import CategoryValidationError

from django.http import (
    Http404
)

from .forms import CategoryForm
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class CategoryBaseView(View):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('category:category')

class CategoryListView(CategoryBaseView, ListView):
    paginate_by = 3
    context_object_name = 'paged_categories'
    template_name = 'category/categories.html'
    # get all category

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context.update({
            'categories_count': self.object_list.count(),
            'all_categories': self.object_list,
        })
        return context

    """View to list all Category.
    Use the 'category_list' variable in the template
    to access all Film objects"""


class CategoryDetailView(HitCountDetailView):
    model = Category
    count_hit = True
    template = 'category/products_by_category.html'
    
    slug_field = 'slug'
    # Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    
    def get_context_data(self,page, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        category = context['category']
        products = category.product_set.all()
        panigator = Paginator(products, 3)
        paged_products = panigator.get_page(page)
        products_count = products.count()

        context.update({
            'category': category,
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


@login_required(login_url='login')
def add_category(request):
    """View to add category"""
    form = CategoryForm(request.POST or None, request.FILES or None)

    context = {
        'type_of_crud':'Add',
        'form':form,
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.owner = request.user
                category.save()
                messages.success(request, 'Category created successfully')
            except ValidationError as e:
                messages.warning(request, e)
    return render(request, 'category/add_edit_category.html', context)

@login_required(login_url='login')
def edit_category(request, category_id):
    category = get_object_or_404(Category,id=category_id)

    if request.user != category.owner:
        raise Http404('Not allow!')

    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)

    context = {
        'form':form,
        'category':category,
        'type_of_crud':'Edit',
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Category updated successfully')
            except ValidationError as e:
                messages.warning(request, e)
    return render(request, 'category/add_edit_category.html', context)


class CategoryDeleteView(CategoryBaseView, DeleteView):
    manage_url = 'user_manage_view'
    
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        manage URL.
        """
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            messages.warning(self.request, "You can not delete this category!")
            return redirect(self.manage_url)
        self.object.delete()
        messages.success(self.request, "Your category has been deleted!")
        return redirect(self.manage_url)

