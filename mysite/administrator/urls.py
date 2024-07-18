from django.urls import path
from . import views

app_name = "administrator"

urlpatterns = [
  path('', views.top, name="top"),
  path('login/', views.admin_login, name="admin_login"),
  path('logout/', views.admin_logout, name="admin_logout"),
  path('itemIndex/', views.itemIndex, name="itemIndex"),
  path('itemDetail/<int:item_id>/', views.ItemDetail, name="itemDetail"),
  path('itemCreate/', views.itemCreate, name="itemCreate"),
  path('itemCreateCommit/', views.ItemCreateCommit, name="itemCreateCommit"),
  path('itemEdit/<int:item_id>/', views.itemEdit, name="itemEdit"),
  path('itemDelete/<int:item_id>/', views.itemDelete, name="itemDelete"),
  path('purchaseIndex/', views.purchaseIndex, name="purchaseIndex"),
]