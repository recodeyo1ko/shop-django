from django.shortcuts import render
from django.shortcuts import redirect
from account.models import User
from . import models
from . import forms
from django.utils import timezone
from .utils import is_login
from django.shortcuts import get_object_or_404
from .models import Purchase, PurchaseDetail

# Create your views here.

def index(request): 
    search_form = forms.SearchForm() 
    #検索Form生成
    return render(request, 'shopping/main.html', locals()) #この環境内で定義されている変数を辞書として取得できる 

def search(request): 
    if request.method == 'GET':
        search_form = forms.SearchForm(request.GET) #GET通信
        
        if search_form.is_valid():
            keyword = request.GET.get('keyword')
            category = int(request.GET.get('category'))
            category_name = models.Category.objects.get(category_id = category).name
            if category == 0: #すべてのカテゴリ
                found_item = models.Item.objects.filter(name__contains=keyword) #filterフィルタの結果条件に一致するオブジェクトが複数ある 
            else:
                found_item = models.Item.objects.filter(category_id=category,name__contains=keyword)
            if found_item:
                form =[]
                for i in found_item:
                    item = {
                        'item_id':i.item_id,
                        'name':i.name,
                        'color':i.color,
                        'price':i.price,
                        'manufacturer':i.manufacturer,
                        'recommended':i. recommended
                        }
                    form.append(item)

                return render(request, 'shopping/searchResult.html',{'form':form,'keyword':keyword,'category_name':category_name}) #form変数を辞書として取得できる
            else:
                message = '見つかりませんでした'
                return render(request, 'shopping/searchResult.html', {'message':message,'keyword':keyword,'category_name':category_name})
        return redirect('shopping:index')
def item_detail(request,item_id):
    try:
        found_item = models.Item.objects.get(item_id=item_id) #getフィルタの結果条件に一致するオブジェクトが一つだけ
        form =[]
        if found_item:
            item_detail = {
                'item_id':item_id,
                'name':found_item.name,
                'color':found_item.color,
                'price':found_item.price,
                'manufacturer':found_item. manufacturer, 
                'stock':found_item.stock
                }
            form.append(item_detail)
            return render(request, 'shopping/itemDetail.html',{'form':form})
    except:
        return redirect('shopping:index')
    
    return redirect('shopping:index')
                
@is_login
def add_to_cart(request):
    if request.method == 'POST': #POST通信
        user_id = request.session['user_id']
        item_id = int(request.POST.get('itemId'))
        amount = int(request.POST.get('amount'))
        item = models.Item.objects.get(item_id=item_id)
        user = User.objects.get(user_id=user_id) #from account.models import Userにより別アプリのモデルが使える
        if models.ItemsInCart.objects.filter(user_id=user_id, item_id=item_id).exists():
            items_in_cart = models.ItemsInCart.objects.get(item_id=item_id, user_id=user_id)
            items_in_cart.amount += int(amount)
            items_in_cart.booked_date = timezone.now()
            items_in_cart.save()
        else:
            item = models.Item.objects.get(item_id=item_id)
            new_cart = models.ItemsInCart() #新しいItemsInCart作成
            new_cart.user = user
            new_cart.item = item
            new_cart.amount = amount
            new_cart.save() #DB書き込み
        return redirect('shopping:cart')
    return redirect('shopping:index')
                
@is_login
def cart(request): 
    user_id = request.session['user_id'] 
    cart_item = models.ItemsInCart.objects.filter(user_id=user_id) 
    if cart_item:
        form =[]
        total_price = 0
        for i in cart_item:
            cart = {
                'item_id':i.item.item_id,
                'name':i.item.name,
                'color':i.item.color,
                'price':i.item.price,
                'manufacturer':i.item.manufacturer,
                'amount':i.amount,
                'stock':i.item.stock
                }
            total_price = total_price + i.item.price*i.amount
            form.append(cart)
    else:
        message = '商品がありません'
        return render(request, 'shopping/cart.html', {'message':message}) 
    return render(request, 'shopping/cart.html', locals()) 

@is_login
def amount_in_cart(request): 
    
    if request.method == 'POST':  # POST通信 
        user_id = request.session['user_id'] 
        item_id = int(request.POST.get('itemId'))
        amount = int(request.POST.get('amount'))
        try:
            item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
            item_in_cart.amount = amount 
            item_in_cart.save()
        except models.ItemsInCart.DoesNotExist:
            pass  # アイテムが存在しない場合は何もしない
    
    return redirect('shopping:cart')
                
@is_login
def remove_from_cart(request, item_id):
    print(  "remove_from_cart")
    user_id = request.session['user_id']
    try:
        item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
    except models.ItemsInCart.DoesNotExist:
        message = '商品がカートに存在しません'
        return redirect('shopping:cart')
    
    return render(request, 'shopping/removeFromCartConfirm.html', {'item': item_in_cart})

@is_login
def remove_from_cart_commit(request):
    
    if request.method == 'POST':
        user_id = request.session['user_id']
        item_id = int(request.POST.get('item_id'))
        try:
            item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
            context = {
                'item_name': item_in_cart.item.name,
                'item_price': item_in_cart.item.price,
                'item_manufacturer': item_in_cart.item.manufacturer,
                'item_amount': item_in_cart.amount
            }
            item_in_cart.delete()
        except models.ItemsInCart.DoesNotExist:
            pass
        return render(request, 'shopping/removeFromCartCommit.html', context)
    
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
def purchase_confirm(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    cart_items = models.ItemsInCart.objects.filter(user_id=user_id)
    
    for item in cart_items:
        if item.amount > item.item.stock:
            user_id = request.session['user_id']
            cart_item = models.ItemsInCart.objects.filter(user_id=user_id)
            if cart_item:
                form = []
                total_price = 0
                for i in cart_item:
                    cart = {
                        'item_id': i.item.item_id,
                        'name': i.item.name,
                        'color': i.item.color,
                        'price': i.item.price,
                        'manufacturer': i.item.manufacturer,
                        'amount': i.amount,
                        'stock': i.item.stock
                    }
                    total_price += i.item.price * i.amount
                    form.append(cart)
            message = '在庫が足りません。'
            return render(request, 'shopping/cart.html', {'message': message, 'form': form})
    
    if not cart_items.exists():
        message = 'カートが空です。'
        return redirect('/shopping/cart/')
    
    total_price = sum(item.item.price * item.amount for item in cart_items)

    if request.method == "POST":
            purchase_form = forms.PurchaseForm(request.POST)
            if purchase_form.is_valid():
                payment_method = purchase_form.cleaned_data['payment_method']
                address_option = request.POST.get('address_option')
                if address_option == 'registered':
                    address = user.address
                else:
                    address = purchase_form.cleaned_data['address']
                return render(request, 'shopping/purchaseConfirm.html', {
                    'cart_items': cart_items,
                    'total_price': total_price,
                    'payment_method': payment_method,
                    'address': address,
                })
    else:
        purchase_form = forms.PurchaseForm()
    
    return render(request, 'shopping/purchaseConfirm.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'purchase_form': purchase_form,
        'user_address': user.address
    })


@is_login
def purchase_commit(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        cart_items = models.ItemsInCart.objects.filter(user_id=user_id)
        if not cart_items.exists():
            message = 'カートが空です。'
            return redirect('shopping:cart')
        
        purchase = models.Purchase(user_id=user_id)
        purchase.total_price = sum(item.item.price * item.amount for item in cart_items)
        address_option = request.POST.get('address_option')
        if address_option == 'registered':
            user = User.objects.get(user_id=user_id)
            purchase.address = user.address
        else:
            purchase.address = request.POST.get('address')
        purchase.payment_method = request.POST.get('payment_method')
        if purchase.payment_method == '0':
            purchase_payment_method = '代金引換'
        elif purchase.payment_method == '1':
            purchase_payment_method = 'クレジットカード'
        else:
            purchase_payment_method = '銀行振込'
        purchase.save()

        purchase_details = []
        for item in cart_items:
            purchase_detail = models.PurchaseDetail(
                purchase=purchase,
                item=item.item,
                amount=item.amount
            )
            purchase_detail.save()
            purchase_details.append(purchase_detail)

            item.item.stock -= item.amount
            item.item.save()
        cart_items.delete()
        return render(request, 'shopping/purchaseCommit.html', {'purchase_details': purchase_details, 'purchase_payment_method': purchase_payment_method, 'purchase_address': purchase.address})
    
    return redirect('shopping:cart')

@is_login
def purchase_history(request):
    user_id = request.session['user_id']
    purchases = models.Purchase.objects.filter(user_id=user_id).order_by('-purchase_date')
    purchase_details = models.PurchaseDetail.objects.filter(purchase__in=purchases)
    
    return render(request, 'shopping/purchaseHistory.html', {'purchases': purchases, 'purchase_details': purchase_details})

@is_login
def purchase_cancel_confirm(request,purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user_id=request.session['user_id'])
    purchase_details = PurchaseDetail.objects.filter(purchase=purchase)

    if request.method == 'POST':
        return redirect('shopping:purchase_cancel', purchase_id=purchase.id)

    return render(request, 'shopping/purchaseCancelConfirm.html', {
        'purchase': purchase,
        'purchase_details': purchase_details
    })
    

@is_login
def purchase_cancel_commit(request, purchase_id):
    user_id = request.session['user_id']
    purchase = get_object_or_404(Purchase, id=purchase_id, user_id=user_id)
    purchase_details = PurchaseDetail.objects.filter(purchase=purchase)


    if request.method == 'POST':
        cancelled_items = []
        for detail in purchase_details:
            detail.item.stock += detail.amount
            detail.item.save()
            cancelled_items.append({
                'name': detail.item.name,
                'color': detail.item.color,
                'manufacturer': detail.item.manufacturer,
                'price': detail.item.price,
                'amount': detail.amount
            })
        purchase.delete()
        return render(request, 'shopping/purchaseCancelCommit.html', {
            'purchase': purchase,
            'cancelled_items': cancelled_items
        })

    return redirect('shopping:purchase_history')