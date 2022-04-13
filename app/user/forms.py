from django import forms
from .models import NomalUser

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=50)

    email = forms.EmailField(max_length=50)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'place': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'place': 'Confirm password'
    }))

    class Meta:
        model = NomalUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Your phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        clean_data = super(RegisterForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match')
            