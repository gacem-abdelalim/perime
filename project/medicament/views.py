from django.shortcuts import render
from .oracle_utils import fetch_medicaments

def medicament_list(request):
    print('edsfds')
    data = fetch_medicaments()  # fetch live from Oracle
    return render(request, "medicament/list.html", {"medicaments": data})
