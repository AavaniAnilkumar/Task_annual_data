"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
import Api.urls
from Api.views import calculate_annual_data,get_annual_data
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(Api.urls)),
    path('calculate/',calculate_annual_data,name='calculate_annual_data'),
    path('getdata/',get_annual_data,name='get_annual_data')
]
