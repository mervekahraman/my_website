from django import forms
from .models import ShippingAddress
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'email', 'address', 'province', 'district', 'zipcode']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'address': 'Address',
            'province': 'Province',
            'district': 'District',
            'zipcode': 'Zip Code',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your province'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your district'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your zip code'}),
        }

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on the card'}), required=True)
    card_num = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Number on the card'}), required=True)
    card_exp = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expire date'}), required=True)
    card_cvv = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cvv number'}), required=True)
    card_type = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card type'}), required=True)
