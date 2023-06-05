"""trainee_reports URL Configuration

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

from trainee_reports.views.home_view import HomeView
from trainee_reports.views.listboard_view import ListBoardView

app_name ='trainee_reports'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home_url', HomeView.as_view(), name='home_url'),
    path('data_manager_listboard_url',ListBoardView.as_view(),name='data_manager_listboard_url')
]
