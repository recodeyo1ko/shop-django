import logging
from django.shortcuts import render, redirect
from . import models
from . import forms
from shopping.models import Item, Purchase, PurchaseDetail, Category
from shopping.forms import SearchForm
from account.models import User
from .utils import is_admin_login
from django.shortcuts import get_object_or_404
from datetime import datetime

logger = logging.getLogger('login') # loggerを指定


@is_admin_login
def top(request):
    if "is_login" in request.session:
        message = "管理者としてログインする場合は、事前に一般ユーザからログアウトしてください"
        return render(request, "shopping/main.html", {"message": message})
    item_search_form = SearchForm() 
    user_search_form = forms.UserSearchForm()
    return render(request, "administrator/main.html", locals())

def admin_login(request):
    if request.method == 'POST':
        login_form = forms.AdminLoginForm(request.POST)  # 管理者用ログインForm生成
        message = '入力した内容を再度確認してください'
        if login_form.is_valid():
            admin_id = login_form.cleaned_data.get('admin_id')
            password = login_form.cleaned_data.get('password')
            try:
                admin = models.Admin.objects.get(admin_id=admin_id)
            except models.Admin.DoesNotExist:
                message = '管理者が存在しません'
                return render(request, 'administrator/login.html', {'login_form': login_form, 'message': message})
            if admin.password == password:
                request.session['admin_is_login'] = True  # session書き込み
                request.session['admin_id'] = admin.admin_id
                logger.info('url:%s method:%s admin:%s login' % (request.path, request.method, admin.admin_id))  # log
                return redirect('administrator:top')  # ログイン成功後、管理者トップページへリダイレクト
            else:
                message = 'パスワードが正しくありません。'
                return render(request, 'administrator/login.html', {'login_form': login_form, 'message': message})
        else:
            return render(request, 'administrator/login.html', {'login_form': login_form, 'message': message})
    login_form = forms.AdminLoginForm()
    return render(request, 'administrator/login.html', {'login_form': login_form})
  
@is_admin_login
def admin_logout(request):
  request.session.flush()
  return redirect("administrator:admin_login")

@is_admin_login
def item_edit(request, item_id):
    item = Item.objects.get(item_id=item_id)
    if request.method == "POST":
        item_form = forms.ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.save()
            return redirect("administrator:item_index")
    else:
        item_form = forms.ItemForm(instance=item)
    return render(request, "administrator/itemEdit.html", {"item_form": item_form})

@is_admin_login
def purchase_index(request):
    purchases = Purchase.objects.all()
    
    user_id = request.GET.get('id', None)
    from_year = int(request.GET.get('fromYear', 0))
    from_month = int(request.GET.get('fromMonth', 0))
    from_day = int(request.GET.get('fromDay', 0))
    to_year = int(request.GET.get('toYear', 0))
    to_month = int(request.GET.get('toMonth', 0))
    to_day = int(request.GET.get('toDay', 0))

    if user_id:
        purchases = purchases.filter(user__user_id=user_id)
    
    if from_year > 0 and from_month > 0 and from_day > 0:
        from_date = datetime(from_year, from_month, from_day)
        purchases = purchases.filter(purchase_date__gte=from_date)
    
    if to_year > 0 and to_month > 0 and to_day > 0:
        to_date = datetime(to_year, to_month, to_day, 23, 59, 59)  # 日付の終わりを含める
        purchases = purchases.filter(purchase_date__lte=to_date)
    
    return render(request, 'administrator/purchaseIndex.html', {'purchases': purchases})

@is_admin_login
def item_search(request):
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        
        if search_form.is_valid():
            keyword = request.GET.get('keyword')
            category = int(request.GET.get('category'))
            category_name = Category.objects.get(category_id = category).name
            if category == 0: #すべてのカテゴリ
                found_item = Item.objects.filter(name__contains=keyword) #filterフィルタの結果条件に一致するオブジェクトが複数ある 
            else:
                found_item = Item.objects.filter(category_id=category,name__contains=keyword)
            if found_item:
                items =[]
                for i in found_item:
                    item = {
                        'item_id':i.item_id,
                        'name':i.name,
                        'category':i.category.name,
                        'color':i.color,
                        'price':i.price,
                        'manufacturer':i.manufacturer,
                        'recommended':i.recommended,
                        'stock':i.stock
                        }
                    items.append(item)

                return render(request, 'administrator/itemSearch.html',{'items':items,'keyword':keyword,'category_name':category_name}) #form変数を辞書として取得できる
            else:
                message = '見つかりませんでした'
                return render(request, 'administrator/itemSearch.html', {'message':message,'keyword':keyword,'category_name':category_name})
        return redirect('administrator:item_search')
    

@is_admin_login
def register_item(request):
    if request.method == 'GET':
        item_form = forms.ItemForm()
    else:
        return redirect('administrator:top')
    return render(request, 'administrator/registerItem.html', {'item_form': item_form})

@is_admin_login
def register_item_confirm(request):
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST)
        if item_form.is_valid():
            item = {
                'name': item_form.cleaned_data['name'],
                'category': item_form.cleaned_data['category'],
                'color': item_form.cleaned_data['color'],
                'price': item_form.cleaned_data['price'],
                'manufacturer': item_form.cleaned_data['manufacturer'],
                'recommended': item_form.cleaned_data['recommended'],
                'stock': item_form.cleaned_data['stock'],
            }
            return render(request, 'administrator/registerItemConfirm.html', {'item': item})
    else:
        item_form = forms.ItemForm()
    return render(request, 'administrator/registerItem.html', {'item_form': item_form})

@is_admin_login
def register_item_commit(request):
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST)
        try:
            if item_form.is_valid():
                item = item_form.save()
                return render(request, 'administrator/registerItemCommit.html', {'item': item})
            else:
                error_messages = []
                for field, errors in item_form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")
                raise Exception("入力内容にエラーがあります。詳細: " + ", ".join(error_messages))
        except Exception as e:
            return render(request, 'administrator/registerItem.html', {'item_form': item_form, 'error_message': str(e)})
    else:
        item_form = forms.ItemForm()
    return render(request, 'administrator/registerItem.html', {'item_form': item_form})


@is_admin_login
def update_item(request, item_id):
    if request.method == 'GET':
        item = Item.objects.get(item_id=item_id)
        form = forms.ItemForm(instance=item)
    else:
        return redirect('administrator:top')
    return render(request, 'administrator/updateItem.html', {'form': form, 'item': item})

@is_admin_login
def update_item_confirm(request, item_id):
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST)
        if item_form.is_valid():
            item_data = item_form.cleaned_data
            item = {
                'item_id': item_id,
                'name': item_data['name'],
                'category_id': item_data['category'].category_id,
                'category_name': item_data['category'].name,
                'color': item_data['color'],
                'price': item_data['price'],
                'manufacturer': item_data['manufacturer'],
                'recommended': item_data['recommended'],
                'stock': item_data['stock'],
            }
            return render(request, 'administrator/updateItemConfirm.html', {'item': item})
    else:
        item = get_object_or_404(Item, item_id=item_id)
        item_form = forms.ItemForm(instance=item)
    return render(request, 'administrator/updateItem.html', {'item_form': item_form, 'item': item})



@is_admin_login
def update_item_commit(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item = item_form.save()
            return render(request, 'administrator/updateItemCommit.html', {'item': item})
        else:
            return render(request, 'administrator/updateItem.html', {'item_form': item_form, 'item': item})
    else:
        return redirect('administrator:update_item', item_id=item_id)

@is_admin_login
def delete_item_confirm(request, item_id):
    item = Item.objects.get(item_id=item_id)
    return render(request, 'administrator/deleteItemConfirm.html', {'item': item})

@is_admin_login
def delete_item_commit(request, item_id):
    item = Item.objects.get(item_id=item_id)
    item.delete()
    return render(request, 'administrator/deleteItemCommit.html', {'item': item})

@is_admin_login
def user_search(request):
    if request.method == 'GET':
        user_search_form = forms.UserSearchForm(request.GET)
        if user_search_form.is_valid():
            user_id = request.GET.get('user_id')
            if user_id:
                users = User.objects.filter(user_id=user_id)
            else:
                users = User.objects.all()
            return render(request, 'administrator/userSearch.html', {'users': users})
        return redirect('administrator:user_search')

@is_admin_login
def update_user(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    user_form = forms.UserForm(instance=user)
    return render(request, 'administrator/updateUser.html', {'user_form': user_form, 'user': user})

@is_admin_login
def update_user_confirm(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    form_data = request.POST
    user_form = forms.UserForm(form_data, instance=user)
    if user_form.is_valid():
        request.session['user_form_data'] = form_data
        return render(request, 'administrator/updateUserConfirm.html', {'user': user})
    else:
        print(user_form.errors)
    return redirect('administrator:update_user', user_id=user_id)


@is_admin_login
def update_user_commit(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    form_data = request.session.pop('user_form_data', None)
    if form_data:
        user_form = forms.UserForm(form_data, instance=user)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'administrator/updateUserCommit.html', {'user': user})
    return redirect('administrator:update_user', user_id=user_id)

@is_admin_login
def delete_user_confirm(request, user_id):
    user = User.objects.get(user_id=user_id)
    return render(request, 'administrator/deleteUserConfirm.html', {'user': user})

@is_admin_login
def delete_user_commit(request, user_id):
    user = User.objects.get(user_id=user_id)
    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'address': user.address,
    }
    user.delete()
    return render(request, 'administrator/deleteUserCommit.html', {'user': user_data})

@is_admin_login
def delete_purchase_confirm(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    purchase_details = PurchaseDetail.objects.filter(purchase_id=purchase_id)
    return render(request, 'administrator/deletePurchaseConfirm.html', {'purchase': purchase, 'purchase_details': purchase_details})

@is_admin_login
def delete_purchase_commit(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    purchase_data = {
        'purchase_id': purchase.id,
        'user_id': purchase.user.user_id,
        'purchase_date': purchase.purchase_date,
    }
    purchase_details = PurchaseDetail.objects.filter(purchase_id=purchase_id).values(
        'item__name', 'item__color', 'item__manufacturer', 'item__price', 'amount'
    )
    context = {
        'purchase': purchase_data,
        'purchase_details': list(purchase_details)
    }
    purchase.delete()
    return render(request, 'administrator/deletePurchaseCommit.html', context)