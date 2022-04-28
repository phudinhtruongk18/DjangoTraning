from django import forms
from .models import Photo, Product


# photos form for product
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)
    
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'categories']
        widgets = {'photos': PhotoForm}

    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter a product Name'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['placeholder'] = 'Enter a product Price'
        self.fields['categories'].widget.attrs['class'] = 'form-control'
