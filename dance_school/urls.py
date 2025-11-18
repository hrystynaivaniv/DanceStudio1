"""
URL configuration for dance_school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from core.views import (
    DanceStyleViewSet, EquipmentViewSet, HallViewSet, HallEquipmentViewSet,
    InstructorViewSet, SubscriptionViewSet, ClientViewSet, ClassViewSet,
    AttendanceViewSet, PaymentViewSet, SubscriptionReportView, HallEquipmentReportView
)
from web import views, views_lab3

router = routers.DefaultRouter()

router.register(r"dance-styles", DanceStyleViewSet, basename="dance-style")
router.register(r"equipment", EquipmentViewSet, basename="equipment")
router.register(r"halls", HallViewSet, basename="hall")
router.register(r"hall-equipment", HallEquipmentViewSet, basename="hall-equipment")
router.register(r"instructors", InstructorViewSet, basename="instructor")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscription")
router.register(r"clients", ClientViewSet, basename="client")
router.register(r"classes", ClassViewSet, basename="class")
router.register(r"attendances", AttendanceViewSet, basename="attendance")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path('players/', views_lab3.player_list, name='player_list_name'),
    path('players/delete/<int:player_id>/', views_lab3.player_delete,
         name='delete_url_name'),
    path('characters/', views_lab3.character_list, name='character_list_name'),
    path('characters/delete/<int:character_id>/', views_lab3.character_delete,
         name='delete_url_name'),

    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("reports/subscriptions/", SubscriptionReportView.as_view(), name="subscription-report"),
    path("reports/hall-equipment/", HallEquipmentReportView.as_view(), name="hall-equipment-report"),
    path('', views.client_list, name='client_list'),
    path('client/<int:pk>/', views.client_detail, name='client_detail'),
    path('client/new/', views.client_create, name='client_create'),
    path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('client/<int:pk>/delete/', views.client_delete, name='client_delete'),
]

