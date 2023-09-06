from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("",views.index, name='index'),
    path("prescription",views.createprescriptionView,name="prescription"),
    path("shop",views.shopView.as_view(), name='shop'),
    path("contact",views.contact, name='contact'),
    path("about",views.about, name='about'),
    path("cart",views.cart, name='cart'),
    path("thankyou",views.thankyou, name='thankyou'),
    path("login",views.login_, name='login'),
    path("signup",views.signup, name='signup'),
    path("checkout",views.checkout,name='checkout'),
    path("singleShop/<int:drug_id>",views.singleshop,name='singleshop'),
    #cart urls
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('logout', views.log_out, name='logout'),
    
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

