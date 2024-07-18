import logging
from django.shortcuts import render, redirect
from . import models
from . import forms
from shopping.models import Item, Purchase, PurchaseDetail, Category
from .utils import is_admin_login

logger = logging.getLogger('login') # loggerを指定


@is_admin_login
def top(request):
    if "is_login" in request.session:
        message = "管理者としてログインする場合は、事前に一般ユーザからログアウトしてください"
        return render(request, "shopping/main.html", {"message": message})
    return render(request, "administrator/top.html")

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
def itemIndex(request):
    items = Item.objects.all()
    return render(request, "administrator/itemIndex.html", {"items": items})

@is_admin_login
def itemCreate(request):
   pass

@is_admin_login
def ItemCreateCommit(request):
    pass
  
@is_admin_login
def ItemDetail(request, item_id):
    item = Item.objects.get(item_id=item_id)
    return render(request, "administrator/itemDetail.html", {"item": item})

@is_admin_login
def itemEdit(request, item_id):
    item = Item.objects.get(item_id=item_id)
    if request.method == "POST":
        item_form = forms.ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.save()
            return redirect("administrator:itemIndex")
    else:
        item_form = forms.ItemForm(instance=item)
    return render(request, "administrator/itemEdit.html", {"item_form": item_form})

@is_admin_login
def itemDelete(request, item_id):
   pass

@is_admin_login
def purchaseIndex(request):
  if "admin_id" in request.session:
    purchases = Purchase.objects.all()
    return render(request, "administrator/purchaseIndex.html", {"purchases": purchases})
  else:
    return redirect("administrator:admin_login")
  
