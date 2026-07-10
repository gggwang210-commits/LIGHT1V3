from django.shortcuts import render

from lightone.services import dashboard_context


def dashboard(request):
    return render(request, 'dashboard/dashboard.html', dashboard_context())
