from django.urls import path
from . import views

urlpatterns = [
    path('',                       views.product_list,    name='index'),
    path('login/',                 views.login_view,      name='login'),
    path('logout/',                views.logout_view,     name='logout'),

    path('products/',                            views.product_list,   name='product_list'),
    path('products/create/',                     views.product_form,   name='product_create'),
    path('products/edit/<str:article>/',         views.product_form,   name='product_edit'),
    path('products/delete/<str:article>/',       views.product_delete, name='product_delete'),

    path('orders/',                              views.order_list,     name='order_list'),
    path('orders/create/',                       views.order_create,   name='order_create'),
    path('orders/edit/<int:order_id>/',          views.order_edit,     name='order_edit'),
    path('orders/delete/<int:order_id>/',        views.order_delete,   name='order_delete'),
]
