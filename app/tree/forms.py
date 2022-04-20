from django import forms
from .models import Comment, Catalog, Product, Photo


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['parent','name','image']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image','num_of_images']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['name']

