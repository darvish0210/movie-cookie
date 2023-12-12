
import re
import json
import urllib
import environ
from pathlib import Path

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)


@csrf_exempt
@api_view(['POST'])
def getMovieInfo(request):
    KMDB_API_KEY = str(env('KMDB_API_KEY'))
    print(request.body)
    query = urllib.parse.quote(request.data['query'])
    url = f"https://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={
        KMDB_API_KEY}&detail=Y&query={query}"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        return Response(dict, status=status.HTTP_200_OK)
    else:
        return Response(rescode, status=status.HTTP_400_BAD_REQUEST)
