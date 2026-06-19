from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import (Category, Manufacturer, Supplier, Product,
                     PickPoint, Order, User)
from .backends import require_role

ROLE_ADMIN, ROLE_MANAGER, ROLE_CLIENT = 1, 2, 3


def _ctx(request):
    return {
        'user_display': request.session.get('store_user_name'),
        'store_user':   request.session.get('store_user_id'),
        'role_id':      request.session.get('store_user_role'),
        'can_manage':   request.session.get('store_user_role') in (ROLE_ADMIN, ROLE_MANAGER),
        'can_admin':    request.session.get('store_user_role') == ROLE_ADMIN,
    }


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        authenticate(request,
                     username=request.POST.get('login'),
                     password=request.POST.get('password'))
        if request.session.get('store_user_id'):
            return redirect('product_list')
        messages.error(request, 'Неверный логин или пароль')
    return render(request, 'store/login.html', _ctx(request))


def logout_view(request):
    for k in ('store_user_id', 'store_user_role', 'store_user_name'):
        request.session.pop(k, None)
    return redirect('login')


@require_role()
def product_list(request):
    qs = Product.objects.select_related('category', 'manufacture', 'suplyer').all()

    q   = request.GET.get('q', '').strip()
    cat = request.GET.get('category')
    man = request.GET.get('manufacturer')
    so  = request.GET.get('sort', '')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(article__icontains=q))
    if cat:
        qs = qs.filter(category_id=cat)
    if man:
        qs = qs.filter(manufacture_id=man)

    sort_map = {
        'price_asc':  'price',
        'price_desc': '-price',
        'name_asc':   'name',
        'name_desc':  '-name',
    }
    qs = qs.order_by(sort_map.get(so, 'name'))

    ctx = _ctx(request)
    ctx.update({
        'products':             qs,
        'categories':           Category.objects.all(),
        'manufacturers':        Manufacturer.objects.all(),
        'current_search':       q,
        'current_sort':         so,
        'current_category':     int(cat) if cat else None,
        'current_manufacturer': int(man) if man else None,
    })
    return render(request, 'store/product_list.html', ctx)


@require_role(ROLE_ADMIN, ROLE_MANAGER)
def product_form(request, article=None):
    is_edit = article is not None
    product = get_object_or_404(Product, pk=article) if is_edit else None

    if request.method == 'POST':
        data = request.POST
        if not is_edit:
            last = Product.objects.order_by('-article').values_list('article', flat=True).first()
            try:
                next_num = int(last) + 1 if last and last.isdigit() else 1
            except ValueError:
                next_num = 1
            product = Product(article=str(next_num).zfill(7))
        product.name           = data.get('name')
        product.unit           = data.get('unit')
        product.price          = data.get('price') or 0
        product.max_discount   = data.get('max_discount') or 0
        product.discount       = data.get('discount') or 0
        product.quantity       = data.get('quantity') or 0
        product.description    = data.get('description')
        product.category_id    = data.get('category')   or None
        product.manufacture_id = data.get('manufacturer') or None
        product.suplyer_id     = data.get('supplier')   or None
        product.image_path     = data.get('image_path')
        product.save()
        return redirect('product_list')

    last = Product.objects.order_by('-article').values_list('article', flat=True).first()
    try:
        next_article = str(int(last) + 1).zfill(7) if last and last.isdigit() else '0000001'
    except ValueError:
        next_article = '0000001'

    ctx = _ctx(request)
    ctx.update({
        'product':       product,
        'categories':    Category.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
        'suppliers':     Supplier.objects.all(),
        'is_edit':       is_edit,
        'next_article':  next_article,
    })
    return render(request, 'store/product_form.html', ctx)


@require_role(ROLE_ADMIN)
def product_delete(request, article):
    get_object_or_404(Product, pk=article).delete()
    return redirect('product_list')


@require_role()
def order_list(request):
    qs = Order.objects.select_related('user', 'product', 'pickpoint').order_by('-order_id')
    if request.session.get('store_user_role') == ROLE_CLIENT:
        qs = qs.filter(user_id=request.session.get('store_user_id'))
    ctx = _ctx(request)
    ctx['orders'] = qs
    return render(request, 'store/order_list.html', ctx)


@require_role(ROLE_CLIENT, ROLE_MANAGER, ROLE_ADMIN)
def order_create(request):
    if request.method == 'POST':
        d = request.POST
        Order.objects.create(
            pickpoint_id   = d.get('pickpoint') or None,
            order_date     = date.today(),
            status         = 'Новый',
            user_id        = request.session.get('store_user_id'),
            article        = d.get('product'),
            quantity       = int(d.get('quantity') or 1),
            pickup_code    = int(d.get('pickup_code') or 0) or None,
        )
        return redirect('order_list')
    ctx = _ctx(request)
    ctx.update({
        'products':         Product.objects.filter(quantity__gt=0),
        'pickpoints':       PickPoint.objects.all(),
        'users':            User.objects.all(),
        'current_datetime': date.today(),
    })
    return render(request, 'store/order_create.html', ctx)


@require_role(ROLE_ADMIN, ROLE_MANAGER)
def order_edit(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        d = request.POST
        order.status         = d.get('status', order.status)
        order.delivery_date  = d.get('delivery_date') or None
        order.quantity       = int(d.get('quantity') or order.quantity)
        order.save()
        return redirect('order_list')
    ctx = _ctx(request)
    ctx.update({'order': order, 'products': Product.objects.all()})
    return render(request, 'store/order_edit.html', ctx)


@require_role(ROLE_ADMIN)
def order_delete(request, order_id):
    get_object_or_404(Order, pk=order_id).delete()
    return redirect('order_list')
