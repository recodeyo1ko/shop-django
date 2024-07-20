from django.urls import path
from . import views

app_name = "administrator"

urlpatterns = [
  path('', views.top, name="top"),
  path('login/', views.admin_login, name="admin_login"),
  path('logout/', views.admin_logout, name="admin_logout"),
  path('itemSearch/', views.item_search, name="item_search"),
  path('userSearch/', views.user_search, name="user_search"),

  # 注文関連
  path('purchaseIndex/', views.purchase_index, name="purchase_index"),
  path('deletePurchaseConfirm/<int:purchase_id>/', views.delete_purchase, name="delete_purchase"),

  # item関連
  path('registerItem/', views.register_item, name="register_item"),
  path('registerItemCommit/', views.register_item_commit, name="register_item_commit"),
  path('updateItem/<int:item_id>/', views.update_item, name="update_item"),
  path('updateItemCommit/<int:item_id>/', views.update_item_commit, name="update_item_commit"),
  path('deleteItemConfirm/<int:item_id>/', views.delete_item, name="delete_item"),

  # user関連
  path('updateUser/<int:user_id>/', views.update_user, name="update_user"),
  path('updateUserCommit/<int:user_id>/', views.update_user_commit, name="update_user_commit"),
  path('deleteUser/<int:user_id>/', views.delete_user, name="delete_user"),

]