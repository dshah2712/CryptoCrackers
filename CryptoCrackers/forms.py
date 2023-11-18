from django import forms
from django.shortcuts import get_object_or_404

from .models import UserDetails, Wallet, CryptoCurrency, Purchase, Transaction


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', required=True)

    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'username', 'date_of_birth', 'id_image', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


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


class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['cryptocurrency', 'quantity']
        widgets = {
            'cryptocurrency': forms.Select(attrs={'id': 'id_cryptocurrency'}),
            'quantity': forms.TextInput(attrs={'id': 'id_quantity'}),
        }

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cryptocurrency'].queryset = CryptoCurrency.objects.all()
        self.user_id = user_id

    def clean(self):
        cleaned_data = super().clean()
        cryptocurrency = cleaned_data.get('cryptocurrency')
        quantity = cleaned_data.get('quantity')


        # wallet = Wallet.objects.get(user_id=self.user_id)
        total_amount = cryptocurrency.current_price_cad * quantity
        #
        # if wallet.balance < total_amount:
        #     raise forms.ValidationError("Insufficient balance to make the purchase.")

        cleaned_data['total_amount'] = total_amount
        # cleaned_data['available_balance'] = wallet.balance
        return cleaned_data
