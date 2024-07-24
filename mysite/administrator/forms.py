from django import forms
from . import models
from shopping.models import Item, Purchase, PurchaseDetail, Category
from account.models import User

class AdminLoginForm(forms.Form):
    admin_id = forms.CharField(
        label="管理者ID",
        max_length=128,
        widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '管理者ID'}
      )
    )
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': 'パスワード'}
      )
    )

class ItemForm(forms.ModelForm):
    
    name = forms.CharField(
          label="商品名",
          max_length=128,
          widget=forms.TextInput(
            attrs={
                'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
                'placeholder': '商品名'}
          )
    )
    manufacturer = forms.CharField(label="メーカー", max_length=32, widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': 'メーカー'}
      )
    )

    color = forms.CharField(label="色", max_length=16, widget=forms.TextInput(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '色'}
      )
    )
    price = forms.IntegerField(label="価格", widget=forms.NumberInput(
    attrs={
        'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '価格'}
      )
    )
    stock = forms.IntegerField(label="在庫数", widget=forms.NumberInput(
    attrs={
        'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': '在庫数'}
      )
    )
    recommended = forms.BooleanField(label="おすすめ商品", required=False, widget=forms.CheckboxInput(
    attrs={
        'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800'}
      )
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="カテゴリ", widget=forms.Select(
    attrs={
        'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800'}
      )
    )

    class Meta:
            model = Item
            fields = ['name', 'manufacturer', 'color', 'price', 'stock', 'recommended', 'category']

class UserSearchForm(forms.Form):
    user_id = forms.IntegerField(label="ユーザID", required=False, widget=forms.NumberInput(
    attrs={
        'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
        'placeholder': 'ユーザID'}
      )
    )
    
    class Meta:
        model = User
        fields = ['user_id']

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
    label="パスワード",
    max_length=256,
    widget=forms.PasswordInput(
      render_value=True, attrs={'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800', 'placeholder': 'パスワード'}
      )
    )
    password2 = forms.CharField(
    label="パスワード(確認)",
    max_length=256,
    widget=forms.PasswordInput(
      render_value=True,
      attrs={'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800', 'placeholder': 'パスワード(確認)'}
      )
    )
    
    name = forms.CharField(
    label="お名前",
    max_length=128,
    widget=forms.TextInput(attrs={'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800', 'placeholder': 'お名前'})
    )

    address = forms.CharField(
    label="ご住所",
    max_length=256,
    widget=forms.TextInput(attrs={'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800', 'placeholder': 'ご住所'})
    )

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'name', 'address']