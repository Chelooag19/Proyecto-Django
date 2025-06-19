from django.contrib import admin
from .models import Cliente, Vehiculo, Servicio, Cita

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Cita)