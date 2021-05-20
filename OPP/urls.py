"""OPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls.conf import include
from OPP import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('official_auth/', include('official_auth.urls')),
    path('official_app/',include('official_app.urls')),

    path('user_auth/', include('user_auth.urls')),
    path('',include('user_app.urls')),

    path('search_offenders_image',views.search_offenders_by_image,name="search_offenders_image"),
    path('search_offenders_name',views.search_offenders_by_name,name="search_offenders_name"),


]
