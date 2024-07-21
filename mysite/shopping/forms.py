from django import forms
from . import models

# 必須機能

class SearchForm(forms.Form):
  category = forms.ModelChoiceField(
    models.Category.objects.order_by(
      'category_id'
    ),
    widget=forms.Select(
      attrs={
        'class': 'w-1/5 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800'
      }
    ),

  label='カテゴリ', to_field_name="category_id", initial='0') 
  keyword = forms.CharField(
    label="キーワード", 
    max_length=128, 
    required = False,
    widget=forms.TextInput(
      attrs={
        'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800', 'placeholder': 'キーワード'}
    )
  )

class PurchaseForm(forms.Form):
    payment_method = forms.ChoiceField(
        label="支払い方法",
        choices=(
            (0, '代金引換'),
        ),
        widget=forms.Select(
            attrs={
                'class': 'w-1/2 px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800'
            }
        )
    )
    address = forms.CharField(
        label="配送先",
        max_length=256,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-3 py-2 border rounded-md dark:border-gray-300 dark:bg-gray-50 dark:text-gray-800',
                'placeholder': '配送先'}
        )
    )