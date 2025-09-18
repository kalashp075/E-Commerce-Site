"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp, name="myapp"),
    path('login_page/', login_page, name="login_page"),
    path('signup_page1/', signup_page1, name="signup_page1"),
    path('signup_page2/', signup_page2, name="signup_page2"),
    path('signup_page3/', signup_page3, name="signup_page3"),
    path('verification/', verification, name="verification"), 
    path('logout/', logout_view, name='logout_view'),
    path('home_page/', home_page, name="home_page"),
    path('resend_verification/', resend_verification, name='resend_verification'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('update_cart/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', checkout, name="checkout"),
    path('remove_cart_item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('contact/', contact, name="contact"), 
    path('about/', about, name="about"), 
    path('profile/', profile, name='profile'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

   