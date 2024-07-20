from django.shortcuts import render
from django.shortcuts import redirect
from account.models import User
from . import models
from . import forms
from django.utils import timezone
from .utils import is_login
from django.shortcuts import get_object_or_404
from .models import Purchase, PurchaseDetail
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request): 
    search_form = forms.SearchForm() 
    return render(request, 'shopping/main.html', locals())

def search(request): 
    if request.method == 'GET':
        search_form = forms.SearchForm(request.GET)
        if search_form.is_valid():
            keyword = request.GET.get('keyword')
            category_id = int(request.GET.get('category'))
            category_name = models.Category.objects.get(category_id = category_id).name
            if category_id == 0:
                items = models.Item.objects.filter(name__contains=keyword)
            else:
                items = models.Item.objects.filter(category_id=category_id, name__contains=keyword)
            if items:
                return render(request, 'shopping/searchResult.html', locals())
            else:
                message = '見つかりませんでした'
                return render(request, 'shopping/searchResult.html', locals())
        return redirect('shopping:index')
    return redirect('shopping:index')

def item_detail(request,item_id):
    try:
        item = models.Item.objects.get(item_id=item_id)
        stock_range = range(1, item.stock + 1)
        return render(request, 'shopping/itemDetail.html', locals())
    except:
        print("item_detail error")
        return redirect('shopping:index')

@is_login
def add_to_cart(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        item_id = int(request.POST.get('itemId'))
        amount = int(request.POST.get('amount'))
        item = models.Item.objects.get(item_id=item_id)
        user = User.objects.get(user_id=user_id)
        if models.ItemsInCart.objects.filter(user_id=user_id, item_id=item_id).exists():
            items_in_cart = models.ItemsInCart.objects.get(item_id=item_id, user_id=user_id)
            items_in_cart.amount += int(amount)
            items_in_cart.booked_date = timezone.now()
            items_in_cart.save()
        else:
            item = models.Item.objects.get(item_id=item_id)
            new_cart = models.ItemsInCart()
            new_cart.user = user
            new_cart.item = item
            new_cart.amount = amount
            new_cart.save()
        return redirect('shopping:cart')
    return redirect('shopping:index')

@is_login
def cart(request): 
    user_id = request.session['user_id'] 
    cart_items = models.ItemsInCart.objects.filter(user_id=user_id) 
    if not cart_items:
        message = '商品がありません'
        return render(request, 'shopping/cart.html', locals())
    total_price = sum(item.item.price * item.amount for item in cart_items)
    return render(request, 'shopping/cart.html', locals()) 

@is_login
def amount_in_cart(request, item_id):
    if request.method == 'POST':
        user_id = request.session['user_id']
        amount = int(request.POST.get('amount'))
        try:
            item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
            item_in_cart.amount = amount
            item_in_cart.save()
        except models.ItemsInCart.DoesNotExist:
            return redirect('shopping:cart')
    
    return redirect('shopping:cart')

@is_login
def remove_from_cart(request, item_id):
    user_id = request.session['user_id']
    try:
        item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
    except models.ItemsInCart.DoesNotExist:
        message = '商品がカートに存在しません'
        return redirect('shopping:cart')
    except MultipleObjectsReturned:
        items_in_cart = models.ItemsInCart.objects.filter(user_id=user_id, item_id=item_id)
        if items_in_cart.exists():
            for item in items_in_cart[1:]:
                item.delete()
        item_in_cart = items_in_cart.first()
        message = '商品が複数カートに存在したため、同一商品を削除しました'
        return render(request, 'shopping/removeFromCartConfirm.html', locals())
    return render(request, 'shopping/removeFromCartConfirm.html', locals())

@is_login
def remove_from_cart_commit(request, item_id):
    if request.method == 'POST':
        user_id = request.session['user_id']
        try:
            item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
            item_in_cart_cache = {
                'name': item_in_cart.item.name,
                'price': item_in_cart.item.price,
                'manufacturer': item_in_cart.item.manufacturer,
                'amount': item_in_cart.amount,
            }
            item_in_cart.delete()
        except models.ItemsInCart.DoesNotExist:
            pass
        return render(request, 'shopping/removeFromCartCommit.html', locals())
    return redirect('shopping:cart')


@is_login
def remove_from_all_cart(request):    
    return render(request, 'shopping/removeFromAllCartConfirm.html')

@is_login
def remove_from_all_cart_commit(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        models.ItemsInCart.objects.filter(user_id=user_id).delete()
        message = 'すべての商品がカートから削除されました'
        return render(request, 'shopping/removeFromAllCartCommit.html', {'message': message})
    
    return redirect('shopping:cart')

@is_login
def purchase(request):
    user_id = request.session['user_id']
    cart_items = models.ItemsInCart.objects.filter(user_id=user_id)
    
    if not cart_items.exists():
        message = 'カートが空です。'
        return render(request, 'shopping/cart.html', locals())

    for cart_item in cart_items:
        if cart_item.amount > cart_item.item.stock:
            message = '在庫が足りません。'
            return render(request, 'shopping/cart.html', locals())
    
    total_price = sum(item.item.price * item.amount for item in cart_items)
    
    if request.method == "POST":
        purchase_form = forms.PurchaseForm()
        return render(request, 'shopping/purchaseConfirm.html', locals())
        
    return render(request, 'shopping/cart.html', locals())


@is_login
def purchase_commit(request):
    user_id = request.session['user_id']
    cart_items = models.ItemsInCart.objects.filter(user_id=user_id)
    if not cart_items.exists():
        message = 'カートが空です。'
        return redirect('shopping:cart')

    if request.method == 'POST':
        purchase = forms.PurchaseForm(request.POST)
        if purchase.is_valid():
            purchase = models.Purchase()
            purchase.user_id = user_id
            purchase.payment_method = request.POST.get('payment_method')
            purchase.total_price = sum(item.item.price * item.amount for item in cart_items)
            address_option = request.POST.get('address_option')
            if address_option == 'registered':
                user = User.objects.get(user_id=user_id)
                purchase.address = user.address
            else:
                purchase.address = request.POST.get('address')
            purchase.save()
            for cart_item in cart_items:
                purchase_detail = models.PurchaseDetail()
                purchase_detail.purchase_id = purchase.id
                purchase_detail.item_id = cart_item.item_id
                purchase_detail.amount = cart_item.amount
                purchase_detail.save()

                cart_item.item.stock -= cart_item.amount
                cart_item.item.save()
        
            cart_items.delete()
            purchase_details = models.PurchaseDetail.objects.filter(purchase_id=purchase.id)

        else:
            message = '入力内容を確認してください'
            return render(request, 'shopping/purchaseConfirm.html', locals())
    
        
        return render(request, 'shopping/purchaseCommit.html', locals())
    
    return redirect('shopping:cart')

@is_login
def purchase_history(request):
    user_id = request.session['user_id']
    purchases = models.Purchase.objects.filter(user_id=user_id).order_by('-purchase_date')
    return render(request, 'shopping/purchaseHistory.html', locals())

@is_login
def purchase_cancel(request,purchase_id):
    user_id = request.session['user_id']
    if not models.Purchase.objects.filter(user_id=user_id, id=purchase_id).exists():
        user_id = request.session['user_id']
        purchases = models.Purchase.objects.filter(user_id=user_id).order_by('-purchase_date')
        message = '購入履歴が見つかりません'
        return render(request, 'shopping/purchaseHistory.html', locals())

    purchase = models.Purchase.objects.get(id=purchase_id)
    purchase_details = PurchaseDetail.objects.filter(purchase_id=purchase.id)

    if request.method == 'POST':
        cancel_purchase_cache = {
            'id': purchase.id,
            'payment_method': purchase.payment_method,
            'address': purchase.address,
            'total_price': purchase.total_price,
            'purchase_date': purchase.purchase_date,
        }
        cancelled_purchase_details_cache = []
        for purchase_detail in purchase_details:
            purchase_detail.item.stock += purchase_detail.amount
            purchase_detail.item.save()
            cancelled_purchase_details_cache.append({
                'name': purchase_detail.item.name,
                'color': purchase_detail.item.color,
                'manufacturer': purchase_detail.item.manufacturer,
                'price': purchase_detail.item.price,
                'amount': purchase_detail.amount,
            })
        purchase.delete()
        return render(request, 'shopping/purchaseCancelCommit.html', locals())

    return render(request, 'shopping/purchaseCancelConfirm.html', locals())
