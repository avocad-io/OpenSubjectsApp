from django.shortcuts import render
from django.http import HttpResponse
from .scripts.bn_downloader import get_subj
from django.http import StreamingHttpResponse, Http404
from django.conf import settings
from wsgiref.util import FileWrapper
from django.core import serializers
from django.contrib.auth.decorators import login_required

import mimetypes
import os
import json
import pandas as pd

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def enhancer_query_bn(request):
    if request.method == 'POST':
        user_query = request.POST['search_query']

        # testowa czesc zeby nie czekac na odp bn
        if user_query == "test":
            with open("response.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return render(request, 'Enhancer/results.html', {"bn_results": data})

        bn_results = get_subj(user_query)
        request.session['bn_response_dict'] = bn_results
        return render(request, 'Enhancer/results.html', {"bn_results": bn_results})

    else:
        return render(request, 'Enhancer/enhancer.html')


def downloadjson(request):
    bn_results = request.session.get('bn_response_dict')
    response = HttpResponse(json.dumps(bn_results, ensure_ascii=False), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=cokolwiek.json'
    return response


def downloadcsv(request):
    bn_results = request.session.get('bn_response_dict')
    df = pd.DataFrame.from_dict(bn_results)
    df.to_csv('df_to_export.csv', index=False)
    with open("df_to_export.csv", 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/csv")
        response['Content-Disposition'] = 'inline; filename=df_to_export.csv'
        return response