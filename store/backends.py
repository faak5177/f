from functools import wraps
from django.shortcuts import redirect
from .models import User


class StoreUserBackend:
    # Авторизация по собственной таблице Users (логин/пароль).
    # Сохраняет user_id в сессии; сам request.user остаётся anonymous.

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.select_related('role').get(login=username, password=password)
        except User.DoesNotExist:
            return None
        if request is not None:
            request.session['store_user_id']   = user.user_id
            request.session['store_user_role'] = user.role_id
            request.session['store_user_name'] = user.full_name
        return None

    def get_user(self, user_id):
        return None


def require_role(*allowed_role_ids):
    # Декоратор для view: пускает только указанные роли.
    def deco(view):
        @wraps(view)
        def wrapper(request, *a, **kw):
            role = request.session.get('store_user_role')
            if role is None:
                return redirect('login')
            if allowed_role_ids and role not in allowed_role_ids:
                return redirect('product_list')
            return view(request, *a, **kw)
        return wrapper
    return deco
