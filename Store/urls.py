
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('pdf', views.render_pdf_view, name='pdf'),
    path('profile', views.profile, name='profile'),
    path('purchase_invice/<int:pid>/', views.purchase_invice, name='purchase_invice'),
    path('sale_invoice/<int:pid>/', views.sale_invoice, name='sale_invoice'),
    path('center_invoice/<int:pid>/', views.center_invoice, name='center_invoice'),
    path('customer_invoice/<int:pid>/', views.customer_invoice, name='customer_invoice'),
    path('make_payment_invoice/<int:pid>/', views.make_payment_invoice, name='make_payment_invoice'),
    path('receive_payment_invoice/<int:pid>/', views.receive_payment_invoice, name='receive_payment_invoice'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('manager_dashbord/', views.manager_dashbord, name='manager_dashbord'),
    path('add_center/', views.add_center, name='add_center'),
    path('add_vendor/', views.add_vendor, name='add_vendor'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('raw_purchase/', views.raw_purchase, name='raw_purchase'),
    path('purchase_milk/', views.purchase_milk, name='purchase_milk'),
    path('sale_milk/', views.sale_milk, name='sale_milk'),
    path('raw_sale/', views.raw_sale, name='raw_sale'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('recive_payment/', views.recive_payment, name='recive_payment'),
    path('center_details/', views.center_details, name='center_details'),
    path("deleteCenterMilk/<int:id>/<int:pid>",views.deleteCenterMilk,name="deleteCenterMilk"),
    path("editCenterMilk/<int:id>/<int:pid>",views.editCenterMilk,name="editCenterMilk"),
    path("deleteCenter/<int:id>/",views.deleteCenter,name="deleteCenter"),
    path("deleteCenterPayment/<int:id>/<int:pid>",views.deleteCenterPayment,name="deleteCenterPayment"),
     path("deleteCustomer/<int:id>",views.deleteCustomer,name="deleteCustomer"),
    path("deleteCustomerPayment/<int:id>/<int:pid>",views.deleteCustomerPayment,name="deleteCustomerPayment"),
    path("deleteExpence/<int:id>/<int:pid>",views.deleteExpence,name="deleteExpence"),
    path("deleteSalePayment/<int:id>/<int:pid>",views.deleteSalePayment,name="deleteSalePayment"),
    path('customer_details/', views.customer_details, name='customer_details'),
    path('view_center/<int:pid>/', views.view_center, name='view_center'),
    path('view_customer/<int:pid>/', views.view_customer, name='view_customer'),
    path('register_customer_ex', views.register_customer_ex, name='register_customer_ex'),
    path('add_customer_ex', views.add_customer_ex, name='add_customer_ex'),
    path('PNL', views.PNL, name='PNL'),
    path('BetweenPNL', views.BetweenPNL, name='BetweenPNL'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)