from django.urls import path
from . import views

app_name = "shopping"

urlpatterns = [
    # 必須機能
    path('', views.index),
    path('search/',views.search), 
    path('item/<int:item_id>/', views.item_detail), 
    path('addToCart/',views.add_to_cart), 
    path('cart/',views.cart), 
    # 任意機能 
    path('amountInCart/',views.amount_in_cart), 
    path('amountInCart/<slug:item_id>/',views.amount_in_cart), 
    path('removeFromCart/<int:item_id>/',views.remove_from_cart), 
    path('removeFromCartCommit/',views.remove_from_cart_commit), 
    path('purchase/',views.purchase), 
    path('purchaseCommit/',views.purchase_commit), 
    path('purchaseHistory/',views.purchase_history), 
    path('purchaseCancel/<int:purchase_id>/',views.purchase_cancel_commit),
    path('updateItemInCart/<int:item_id>/',views.updateItemInCart),
]