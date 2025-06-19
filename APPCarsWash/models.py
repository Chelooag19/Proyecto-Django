from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    telefono = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.user.get_full_name()

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30)
    doc_vehiculo = models.BooleanField(default=False)

    def __str__(self):
        return self.patente

class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    valor = models.FloatField()

    def __str__(self):
        return f"{self.nombre} - ${self.valor}"

class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.CharField(max_length=20)
    observaciones = models.TextField()

    def __str__(self):
        return f"{self.cliente.user.username} - {self.servicio}"
