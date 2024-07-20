from django.urls import path
from . import views

app_name = "shopping"

urlpatterns = [
    # 必須機能
    path('', views.index, name='index'),
    path('search/',views.search, name='search'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('addToCart/',views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart, name='cart'),

    # カート内商品の数量変更
    path('amountInCart/<int:item_id>/',views.amount_in_cart, name='amount_in_cart'),

    # カート内商品の削除
    path('removeFromCart/<int:item_id>/',views.remove_from_cart, name='remove_from_cart'),
    path('removeFromCartCommit//<int:item_id>/',views.remove_from_cart_commit, name='remove_from_cart_commit'),
    path('removeFromAllCart/',views.remove_from_all_cart, name='remove_from_all_cart'),
    path('removeFromAllCartCommit/',views.remove_from_all_cart_commit, name='remove_from_all_cart_commit'),

    # 購入
    path('purchase/',views.purchase, name='purchase'),
    path('purchaseCommit/',views.purchase_commit, name='purchase_commit'),
    path('purchaseHistory/',views.purchase_history, name='purchase_history'),
    path('purchaseCancel/<int:purchase_id>/',views.purchase_cancel, name='purchase_cancel'),

]