from django import forms
from .models import UserDetails, Transactions


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),required= True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', required=True)

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'username', 'date_of_birth',  'id_image', 'email', 'password' ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(),required=True)


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


def _init_(self, *args, **kwargs):
    super(RegisterForm, self)._init_(*args, **kwargs)
    self.fields['first_name'].required = True
    self.fields['last_name'].required = True
    self.fields['email'].required = True
    self.fields['username'].required = True
    self.fields['date_of_time'].required = True

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['currency', 'amount']
        widgets = {
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }