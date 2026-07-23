from django.urls import path

from . import views

urlpatterns = [

    path("", views.dashboard),

    path("status/", views.status),

    path("pump/on/", views.pump_on),

    path("pump/off/", views.pump_off),

    path("valve/<int:angle>/", views.valve),

]