# import django.forms.widgets
# from django.forms import ModelForm, Textarea, TextInput, ChoiceField
# from Shop.models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile


class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
                             required=False)
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                 required=False)
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. ' \
                                    'Letters, digits and @/./+/-/_ only.</small></span>'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. ' \
                                    'Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar ' \
                                     'to your other personal information.</li><li>Your password must contain at least ' \
                                     '8 characters.</li><li>Your password can\'t be a commonly used ' \
                                     'password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, ' \
                                     'for verification.</small></span>'


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
                            required=False)
    address = forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
                              required=False)
    province = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'province'}),
                               required=False)
    district = forms.CharField(label="",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'district'}),
                               required=False)
    zipcode = forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zipcode'}),
                              required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address', 'province', 'district', 'zipcode')

#
# class CustomerForm(ModelForm):
#     class Meta:
#         model = Customer
#         fields = ["name"]
#         widgets = {
#             "name": TextInput(attrs={"size": 20}),
#             "email": TextInput(attrs={"size": 50}),
#             "phone_num": TextInput(attrs={"size": 17})
#         }
#         help_texts = {
#             "email": "Please provide a valid email address.",
#             "phone_num": "Enter your phone number in the format XXX-XXX-XXXX.",
#         }
#         widgets = {
#             "name": forms.TextInput(attrs={"size": 20}),
#             "email": forms.EmailInput(),
#             "phone_num": forms.TextInput(attrs={"pattern": "[0-9]{3}-[0-9]{3}-[0-9]{4}"}),
#         }
#
#     def clean_phone_num(self):
#         phone_num = self.cleaned_data["phone_num"]
#         # Custom phone number validation logic here
#         return phone_num
