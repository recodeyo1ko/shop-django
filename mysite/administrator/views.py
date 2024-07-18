import logging
from django.shortcuts import render, redirect
from . import models
from . import forms
from shopping.models import Item, Purchase, PurchaseDetail, Category
from shopping.forms import SearchForm
from .utils import is_admin_login

logger = logging.getLogger('login') # loggerを指定


@is_admin_login
def top(request):
    if "is_login" in request.session:
        message = "管理者としてログインする場合は、事前に一般ユーザからログアウトしてください"
        return render(request, "shopping/main.html", {"message": message})
    
    search_form = SearchForm() 
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
  if "admin_id" in request.session:
    purchases = Purchase.objects.all()
    return render(request, "administrator/purchaseIndex.html", {"purchases": purchases})
  else:
    return redirect("administrator:admin_login")
  

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
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST)
        if item_form.is_valid():
            item_form.save()
            return redirect('administrator:top')
    else:
        item_form = forms.ItemForm()
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
    item = Item.objects.get(item_id=item_id)
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.save()
            return redirect('administrator:top')
    else:
        item_form = forms.ItemForm(instance=item)
    return render(request, 'administrator/updateItem.html', {'item_form': item_form})

@is_admin_login
def update_item_confirm(request, item_id):
    item = Item.objects.get(item_id=item_id)
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            return render(request, 'administrator/updateItemConfirm.html', {'item': item})
    else:
        item_form = forms.ItemForm(instance=item)
    return render(request, 'administrator/updateItem.html', {'item_form': item_form})

@is_admin_login
def update_item_commit(request, item_id):
    item = Item.objects.get(item_id=item_id)
    if request.method == 'POST':
        item_form = forms.ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.save()
            return redirect('administrator:top')
    else:
        item_form = forms.ItemForm(instance=item)
    return render(request, 'administrator/updateItem.html', {'item_form': item_form})


@is_admin_login
def delete_item_confirm(request, item_id):
    item = Item.objects.get(item_id=item_id)
    return render(request, 'administrator/deleteItemConfirm.html', {'item': item})

@is_admin_login
def delete_item_commit(request, item_id):
    item = Item.objects.get(item_id=item_id)
    item.delete()
    return render(request, 'administrator/deleteItemCommit.html', {'item': item})
