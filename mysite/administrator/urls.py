from django.urls import path
from . import views

app_name = "administrator"

urlpatterns = [
  path('', views.top, name="top"),
  path('login/', views.admin_login, name="admin_login"),
  path('logout/', views.admin_logout, name="admin_logout"),
  path('itemSearch/', views.item_search, name="item_search"),
  path('itemEdit/<int:item_id>/', views.item_edit, name="item_edit"),
  path('purchaseIndex/', views.purchase_index, name="purchase_index"),
  path('registerItem/', views.register_item, name="register_item"),
  path('registerItemCommit/', views.register_item_commit, name="register_item_commit"),
  path('registerItemConfirm/', views.register_item_confirm, name="register_item_confirm"),
  path('updateItem/<int:item_id>/', views.update_item, name="update_item"),
  path('updateItemCommit/<int:item_id>/', views.update_item_commit, name="update_item_commit"),
  path('updateItemConfirm/<int:item_id>/', views.update_item_confirm, name="update_item_confirm"),
  path('deleteItemConfirm/<int:item_id>/', views.delete_item_confirm, name="delete_item_confirm"),
  path('deleteItemCommit/<int:item_id>/', views.delete_item_commit, name="delete_item_commit"),
]