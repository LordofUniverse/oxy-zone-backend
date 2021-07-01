"""covidproject URL Configuration

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
from django.urls import path, include
from rest_framework import routers
from frontend import views

from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve

router = routers.DefaultRouter()
router.register(r'sellers', views.SellersView, 'sellers')
router.register(r'places', views.PlacesView, 'places')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('details/', include(router.urls))  #for displaying sellers and places as json in website
    path('api/sellers/login/', views.SellersLoginView.as_view()),
    path('api/sellers/signup/', views.SellersSignupView.as_view()),
    path('api/sellers/details/', views.SellersdetailsView.as_view()),
    path('api/sellers/fulldetails/', views.PlaceswithemailnameView.as_view()),
    path('api/sellers/delete/', views.SellersdeleteView.as_view()),
    path('api/sellers/save/new/', views.SellerssavenewView.as_view()),
    path('api/sellers/save/old/', views.SellerssaveoldView.as_view()),
    path('api/sellers/update/', views.SellersUpdateView.as_view()),
    #path('api/try/', views.SellerstryView.as_view()),
    path('api/getnamebyid/', views.Sellersdetailsbyid.as_view()),
    path('api/getdetbyemail/', views.Sellersdetails2.as_view()),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
