from django.urls import path
from .views import download_quarterly_data

urlpatterns = [

    path('download/',download_quarterly_data,name='download_quarterly_data')
]