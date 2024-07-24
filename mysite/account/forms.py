from django import forms

class UserForm(forms.Form):
  id = forms.CharField(
    label="会員ID",
    max_length=128,
    widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '会員ID'}
      )
    )
  
  password = forms.CharField(
    label="パスワード",
    max_length=256,
    widget=forms.PasswordInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '1234'}
      )
    )
  
class RegisterForm(forms.Form):
  id = forms.CharField(
    label="会員ID",
    max_length=128,
    widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '1234'})
    )
  password1 = forms.CharField(
    label="パスワード",
    max_length=256,
    widget=forms.PasswordInput(
      render_value=True,
      attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': 'xxxx'}
      )
    )
  password2 = forms.CharField(
    label="パスワード(確認)",
    max_length=256,
    widget=forms.PasswordInput(
      render_value=True,
      attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': 'xxxx'}
      )
    )
  name = forms.CharField(
    label="お名前",
    max_length=128,
    widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': 'お名前'})
    )
  address = forms.CharField(
    label="ご住所",
    max_length=256,
    widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '住所'})
    )