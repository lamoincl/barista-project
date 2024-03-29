"""
URL configuration for barista project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from barista.views import HomeView, InjectionView, ResearchView, Request1View,  Request2View, Request3View, ResultView, GenerationView, GenerationResultView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('injection/<str:db_name>/', InjectionView.as_view(), name='injection_url'),
    path('generation/result', GenerationResultView.as_view(), name='generation_result_url'),
    path('generation/', GenerationView.as_view(), name='generation_url'),
    path('recherche/<str:db_name>/', ResearchView.as_view(), name='recherche_url'),
    path('recherche/<str:db_name>/req1', Request1View.as_view(), name='recherche1_url'),
    path('recherche/<str:db_name>/req2', Request2View.as_view(), name='recherche2_url'),
    path('recherche/<str:db_name>/req3', Request3View.as_view(), name='recherche3_url'),
    path('result/', ResultView.as_view(), name='result_url'),

]
