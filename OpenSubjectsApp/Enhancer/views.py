from django.shortcuts import render
from django.http import HttpResponse
from .scripts.bn_downloader import get_subj
from django.http import StreamingHttpResponse, Http404
from django.conf import settings
from wsgiref.util import FileWrapper
from django.core import serializers
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient

import mimetypes
import os
import json
import pandas as pd


def enhancer_query_bn(request):
    if request.method == 'POST':
        #test
        mycol.insert_one(test_dict)
        #test
        user_query = request.POST['search_query']
        bn_results = get_subj(user_query)
        request.session['bn_response_dict'] = bn_results
        return render(request, 'Enhancer/results.html', {"bn_results": bn_results})

    else:
        return render(request, 'Enhancer/enhancer.html')


def downloadjson(request):
    bn_results = request.session.get('bn_response_dict')
    response = HttpResponse(json.dumps(bn_results, ensure_ascii=False), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=results.json'
    return response


def downloadcsv(request):
    bn_results = request.session.get('bn_response_dict')
    df = pd.DataFrame.from_dict(bn_results)
    response = HttpResponse(content_type="application/csv")
    response['Content-Disposition'] = 'inline; filename=results.csv'
    df.to_csv(path_or_buf=response, index=False)
    return response


client = MongoClient(host='localhost',
                    port=27017
                    )
db_handle = client['testdb']
mycol = db_handle['testcol']

test_dict = {'kto': 'Patryk Hubar',
            'czy spóźniony': 'ciągle True'}