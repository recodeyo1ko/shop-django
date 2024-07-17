from django.shortcuts import render
from django.shortcuts import redirect
from account.models import User
from . import models
from . import forms
from django.utils import timezone

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
        return redirect('/shopping/') 
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
        return redirect('/shopping/')
    
    return redirect('/shopping/') 
                
                
def add_to_cart(request):
    if not request.session.get('is_login', None): #ログイン状態確認
        return redirect("/account/login/")
    if request.method == 'POST': #POST通信
        user_id = request.session['user_id']
        item_id = int(request.POST.get('itemId'))
        amount = int(request.POST.get('amount'))
        user = User.objects.get(user_id=user_id) #from account.models import Userにより別アプリのモデルが使える
        if models.ItemsInCart.objects.filter(item_id=item_id).exists():
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
        return redirect('/shopping/cart/')
    return redirect('/shopping/') 
                
def cart(request): 
    if not request.session.get('is_login', None):
        return redirect("/account/login/") 
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

def amount_in_cart(request): 
    if not request.session.get('is_login', None):
        return redirect("/account/login/") 
    if request.method == 'POST': #POST通信 
        user_id = request.session['user_id'] 
        item_id = int(request.POST.get('itemId'))
        amount = int(request.POST.get('amount'))
        item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
    if item_in_cart:
        item_in_cart.amount = amount 
        item_in_cart.save()
    return redirect('/shopping/cart/')

def updateItemInCart(request,item_id):
    if not request.session.get('is_login', None):
        return redirect("/account/login/") 
    if request.method == 'POST': #POST通信 
        user_id = request.session['user_id'] 
        item_id = int(request.POST.get('itemId'))
        amount = int(request.POST.get('amount'))
        item_in_cart = models.ItemsInCart.objects.get(user_id=user_id, item_id=item_id)
    if item_in_cart:
        item_in_cart.amount = amount 
        item_in_cart.save()
    return redirect('/shopping/cart/')
                
def remove_from_cart(request,item_id):
    pass #任意機能 

def remove_from_cart_commit(request):
    pass  # 任意機能 
    
def purchase(request): 
    pass # 任意機能

def purchase_commit(request): 
    pass # 任意機能 

def purchase_history(request): 
    pass # 任意機能 
                
def purchase_cancel(request,purchase_id):
    pass # 任意機能 

def purchase_cancel_commit(request):
    pass # 任意機能