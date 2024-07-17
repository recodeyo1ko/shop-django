from django import forms
from . import models

# 必須機能

class SearchForm(forms.Form):
  category = forms.ModelChoiceField(
    models.Category.objects.order_by('category_id'
    ), 

  label='カテゴリ', to_field_name="category_id", initial='0') 
  keyword = forms.CharField(
    label="キーワード", 
    max_length=128, 
    required = False
    )
