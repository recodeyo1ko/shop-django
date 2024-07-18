from django.urls import path
from . import views

app_name = "administrator"

urlpatterns = [
  path('', views.top, name="top"),
  path('login/', views.admin_login, name="admin_login"),
  path('logout/', views.admin_logout, name="admin_logout"),
  path('itemIndex/', views.item_index, name="item_index"),
  path('itemDetail/<int:item_id>/', views.item_detail, name="item_detail"),
  path('itemCreate/', views.item_create, name="item_create"),
  path('itemCreateCommit/', views.item_create_commit, name="item_create_commit"),
  path('itemEdit/<int:item_id>/', views.item_edit, name="item_edit"),
  path('itemDelete/<int:item_id>/', views.item_delete, name="item_delete"),
  path('purchaseIndex/', views.purchase_index, name="purchase_index"),
]