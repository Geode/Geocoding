# -*- coding: utf-8 -*-
from django.shortcuts import render

from geocoding.form import GeocodingForm
from geocoding.factories import ParserFactory

from django.http import JsonResponse

def AutocompleteAdresse(request):
    if request.method == 'GET':
        adr = request.GET.get('adr', '')
        if(adr):
            parser = ParserFactory().createParser('bxl')
            data = parser.getAddresses(adr)
            return JsonResponse(data)
        else:
            return JsonResponse({})

def test(request):

    form = GeocodingForm()

    return render(request,'geocoding/geocoding.html',{
        'form' : form,
    })
