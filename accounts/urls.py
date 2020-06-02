from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:id>', views.customer, name='customer'),
    path('multiple_order/<str:customer_key>', views.createMultipleOrder, name='multiple_order_for_customer'),
    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:id>', views.updateOrder, name='update_order'),
    path('remove_order/<str:id>', views.removeOrder, name='remove_order'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='user_logout'),
    path('registration/', views.registration, name='register'),
    path('user_page/', views.uesrPage, name='user_page')

]
