"""seshnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from nets import views as net_views
from users import views as users_views
from directmessage import views as dm_views
# from directmessage import routing as dmrouting

# For testing images
from django.conf import settings
from django.conf.urls.static import static

# For login and logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', net_views.home, name='home'),
    path('signup/', users_views.signup, name='signup'),
    path('settings/', users_views.settings, name='settings'),
    path('adminsettings/', users_views.adminsettings, name="adminsettings"),
    path('profile/', users_views.profile, name='profile'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='nets/home.html'), name='logout'),
    path('net/index/', net_views.index, name='net_index'),
    path('net/<str:net_id>/', net_views.net, name='net'),
    path('net/<str:net_id>/save_image_message/', net_views.save_image_form, name="net_save_image"),
    path('net/<str:net_id>/get_messages/', net_views.get_messages, name="net_get_messages"),
    path('net/<str:net_id>/delete_message/', net_views.delete_message, name="net_delete_message"),
    path('directmessage/index/', dm_views.index, name='dm_index'),
    path('directmessage/<str:dc_id>/', dm_views.directmessage, name='directmessage'),
    path('directmessage/<str:dc_id>/save_image_message/', dm_views.save_image_form, name="dm_save_image"),
    path('directmessage/<str:dc_id>/get_messages/', dm_views.get_messages, name="dm_get_messages"),
    path('directmessage/<str:dc_id>/delete_message/', dm_views.delete_message, name="dm_delete_message"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)