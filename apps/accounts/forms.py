from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'password',
            'username',
            'last_name',
            'first_name',
            'is_staff',
            'email',
        ]
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'c-input', 'name': 'password'}),
            'username': forms.TextInput(attrs={'class': 'c-input', 'name': 'username', 'placeholder': 'username'}),
            'first_name': forms.TextInput(attrs={'class': 'c-input', 'name': 'first_name',
                                                 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'c-input', 'name': 'last_name', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'c-input', 'name': 'email', 'placeholder': 'email address'}),
        }


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = '***********'
        self.fields['password2'].widget.attrs['placeholder'] = '***********'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'c-input'
            visible.field.widget.attrs['required'] = ''


class smsCodeVerifyForm(forms.Form):
    Verification_Code = forms.CharField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                                      'placeholder': 'Enter Code Received', 'required':''}))


class forgotPasswordForm(forms.Form):
    Mobile_Number = forms.CharField(widget=forms.TextInput(attrs={'class': 'c-input', 'placeholder': '07xxxxxxxx', 'required':''}))


class passResetCodeVerify(forms.Form):
    Verification_Code = forms.CharField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                                      'placeholder': 'Enter Code Received', 'required':''}))


class SetPasswordForm(forms.Form):
    New_Password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'c-input', 'placeholder': '*************'}))
    Confirm_New_Password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'c-input',
                                                                      'placeholder': '*************', 'required':''}))
