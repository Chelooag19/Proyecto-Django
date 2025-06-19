from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente, Vehiculo, Cita
from .forms import VehiculoForm, CitaForm, CustomUserCreationForm
from django.views.generic import ListView
from django.views import View
from django.shortcuts import redirect


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(user=user, telefono='', fecha_nacimiento='2000-01-01')
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

class CustomLogoutView(View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')


@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'empleado/dashboard.html')
    return render(request, 'cliente/dashboard.html')

@login_required
def registrar_vehiculo(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, "Debes registrarte primero.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.cliente = cliente
            vehiculo.save()
            return redirect('dashboard')
    else:
        form = VehiculoForm()
    return render(request, 'cliente/registrar_vehiculo.html', {'form': form})

@login_required
def registrar_cita(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, "Debes completar tu registro como cliente.")
        return redirect('dashboard')

    
    vehiculos = Vehiculo.objects.filter(cliente=cliente)
    if not vehiculos.exists():
        messages.error(request, "Debes registrar un vehículo antes de agendar una cita.")
        return redirect('registrar_vehiculo')

    if request.method == 'POST':
        form = CitaForm(request.POST)
       
        form.fields['vehiculo'].queryset = vehiculos
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = cliente
            cita.save()
            messages.success(request, "Cita agendada correctamente.")
            return redirect('mis_citas')
    else:
        form = CitaForm()
        form.fields['vehiculo'].queryset = vehiculos

    return render(request, 'cliente/registrar_cita.html', {'form': form})

@login_required
def mis_citas(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    citas = Cita.objects.filter(cliente=cliente)
    return render(request, 'cliente/mis_citas.html', {'citas': citas})

@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, cliente__user=request.user)
    if request.method == 'POST':
        cita.delete()
        return redirect('mis_citas')
    return render(request, 'cliente/cancelar_cita.html', {'cita': cita})

@login_required
def ver_todas_las_citas(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    citas = Cita.objects.all()
    return render(request, 'empleado/todas_las_citas.html', {'citas': citas})

class ServiciosPublicosView(ListView):
    model = Cita
    template_name = 'publico/servicios.html'
    context_object_name = 'servicios'