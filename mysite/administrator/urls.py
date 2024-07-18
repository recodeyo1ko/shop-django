from django.urls import path
from . import views

app_name = "administrator"

urlpatterns = [
  path('', views.top, name="top"),
  path('login/', views.admin_login, name="admin_login"),
  path('logout/', views.admin_logout, name="admin_logout"),
  path('itemSearch/', views.item_search, name="item_search"),
  path('userSearch/', views.user_search, name="user_search"),

  path('purchaseIndex/', views.purchase_index, name="purchase_index"),
  path('registerItem/', views.register_item, name="register_item"),

  # item関連
  path('registerItemCommit/', views.register_item_commit, name="register_item_commit"),
  path('registerItemConfirm/', views.register_item_confirm, name="register_item_confirm"),
  path('updateItem/<int:item_id>/', views.update_item, name="update_item"),
  path('updateItemCommit/<int:item_id>/', views.update_item_commit, name="update_item_commit"),
  path('updateItemConfirm/<int:item_id>/', views.update_item_confirm, name="update_item_confirm"),
  path('deleteItemConfirm/<int:item_id>/', views.delete_item_confirm, name="delete_item_confirm"),
  path('deleteItemCommit/<int:item_id>/', views.delete_item_commit, name="delete_item_commit"),


  # user関連
  path('updateUser/<int:user_id>/', views.update_user, name="update_user"),
  path('updateUserCommit/<int:user_id>/', views.update_user_commit, name="update_user_commit"),
  path('updateUserConfirm/<int:user_id>/', views.update_user_confirm, name="update_user_confirm"),
  path('deleteUserConfirm/<int:user_id>/', views.delete_user_confirm, name="delete_user_confirm"),
  path('deleteUserCommit/<int:user_id>/', views.delete_user_commit, name="delete_user_commit"),
]