from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['parent','name','image']

    def __init__(self,*args,**kwargs):
        super(CategoryForm, self).__init__(*args,**kwargs)
        self.fields['parent'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Enter a Category Name'
        self.fields['name'].widget.attrs['class'] = 'form-control'
