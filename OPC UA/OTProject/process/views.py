from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .api import proces


def dashboard(request):
    return render(request, "dashboard.html")


def status(request):
    return JsonResponse(proces.get_status())


@require_POST
def pump_on(request):
    proces.set_pomp(True)
    return JsonResponse({"success": True})


@require_POST
def pump_off(request):
    proces.set_pomp(False)
    return JsonResponse({"success": True})


@require_POST
def valve(request, angle):
    proces.set_klep_hoek(float(angle))
    return JsonResponse({"success": True})