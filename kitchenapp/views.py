from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from .models import Resident


@login_required
def front_page(request):
    return render(request, "front_page.html")


# def resident_page(request):
#     resident = Resident.objects.get(user=request.user)
#     return render(request, 'resident_page.html', {'resident': resident})
#
#
# def accounting(request):
#     return HttpResponse("You are at the accounting page.")
