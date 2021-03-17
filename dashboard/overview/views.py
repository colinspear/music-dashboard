from django.shortcuts import render
from django.http import HttpResponse


def i_exist(request):
    return HttpResponse('Indeed, this view exists')


