from django import forms
from . import models

# 必須機能

class SearchForm(forms.Form):
  category = forms.ModelChoiceField(
    models.Category.objects.order_by(
      'category_id'
    ), 

  label='カテゴリ', to_field_name="category_id", initial='0') 
  keyword = forms.CharField(
    label="キーワード", 
    max_length=128, 
    required = False
    )

class PurchaseForm(forms.Form):
    payment_method = forms.ChoiceField(
        label="支払い方法",
        choices=(
            (0, '代金引換'),
        )
    )
    address = forms.CharField(
        label="配送先",
        max_length=256,
        required=False
    )