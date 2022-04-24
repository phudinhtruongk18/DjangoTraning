from django import forms
from .models import Catalog

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['parent','name','image']
