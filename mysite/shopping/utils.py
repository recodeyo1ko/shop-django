from django.shortcuts import redirect

def is_login(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if "is_login" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/account/login/") 
    return _wrapped_view_func
