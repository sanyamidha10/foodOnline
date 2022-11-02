from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),

]


#myAccount will decide which user is this vendor or customer, according to it, this will send user to customerDashboard or vendorDashboard