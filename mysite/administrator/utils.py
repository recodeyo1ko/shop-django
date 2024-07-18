from django.shortcuts import redirect

def is_admin_login(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if "admin_id" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("administrator:admin_login")
    return _wrapped_view_func