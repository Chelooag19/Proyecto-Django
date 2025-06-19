from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from APPCarsWash import views
from django.shortcuts import redirect
from django.views import View
from APPCarsWash.views import CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar_vehiculo/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('registrar_cita/', views.registrar_cita, name='registrar_cita'),
    path('mis_citas/', views.mis_citas, name='mis_citas'),
    path('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('todas_las_citas/', views.ver_todas_las_citas, name='todas_las_citas'),
    path('servicios/', views.ServiciosPublicosView.as_view(), name='servicios_publicos'),
]
