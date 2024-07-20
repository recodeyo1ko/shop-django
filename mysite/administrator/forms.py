from django import forms
from . import models
from shopping.models import Item, Purchase, PurchaseDetail, Category
from account.models import User

class AdminLoginForm(forms.Form):
    admin_id = forms.CharField(label="管理者ID", max_length=128)
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)


class ItemForm(forms.ModelForm):
    
    name = forms.CharField(label="商品名", max_length=128)
    manufacturer = forms.CharField(label="メーカー", max_length=32)
    color = forms.CharField(label="色", max_length=16)
    price = forms.IntegerField(label="価格")
    stock = forms.IntegerField(label="在庫数")
    recommended = forms.BooleanField(label="おすすめ商品", required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="カテゴリ")

    class Meta:
            model = Item
            fields = ['name', 'manufacturer', 'color', 'price', 'stock', 'recommended', 'category']

class UserSearchForm(forms.Form):
    user_id = forms.IntegerField(label="ユーザID", required=False)
    
    class Meta:
        model = User
        fields = ['user_id']

class UserForm(forms.ModelForm):
    password1 = forms.CharField(
    label="パスワード",
    max_length=256,
    widget=forms.PasswordInput(
      render_value=True, attrs={'class': 'form-control'}
      )
    )
    password2 = forms.CharField(
    label="パスワード(確認)",
    max_length=256,
    widget=forms.PasswordInput(
      render_value=True,
      attrs={'class': 'form-control' }
      )
    )
    
    name = forms.CharField(
    label="お名前",
    max_length=128,
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    address = forms.CharField(
    label="ご住所",
    max_length=256,
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'name', 'address']