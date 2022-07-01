from django.shortcuts import render
from django.http import HttpResponse
from .scripts.bn_downloader import get_subj
from django.http import StreamingHttpResponse, Http404
from django.conf import settings
from wsgiref.util import FileWrapper
from django.core import serializers

import mimetypes
import os
import json
import pandas as pd

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def enhancer_query_bn(request):
    if request.method == 'POST':
        user_query = request.POST['search_query']

        # testowa czesc zeby nie czekac na odp bn
        if user_query == "test":
            with open("response1.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return render(request, 'Enhancer/results.html', {"bn_results": data})

        #to jest brzydkie i trzeba to zmienić
        bn_results = get_subj(user_query)
        bn_results_json = json.loads(bn_results)
        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(bn_results_json, f, ensure_ascii= False)
        with open("response1.json", "w", encoding="utf-8") as f:
            json.dump(bn_results, f, ensure_ascii= False)
        #return HttpResponse(bn_results,content_type="application/json")
        return render(request, 'Enhancer/results.html', {"bn_results": bn_results})

    else:
        return render(request, 'Enhancer/enhancer.html')


def downloadjson(request):
    with open("response1.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=export.json'
    return response


def downloadcsv(request):
    with open("df_to_export.csv", 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/csv")
        response['Content-Disposition'] = 'inline; filename=df_to_export.csv'
        return response