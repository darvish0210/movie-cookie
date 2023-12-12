import json
import re

from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import MovieInfo
from .serializers import MovieInfoSerializers
from . import utils


class SerachMovieInDB(APIView):
    def post(self, request):
        query = json.loads(request.body)["query"]
        query = re.sub(" ", "", query)
        # queryset = MovieInfo.objects.filter(Q(searchTitle__icontains=query))
        # if not queryset:
        res = utils.getMovieInfo(query)
        data = res.data
        print(data)
        if data["Data"][0]["Count"] == 0:
            return Response({"message": "검색 결과가 없습니다."})

        utils.saveMovieInfo(data)
        queryset = MovieInfo.objects.filter(Q(searchTitle__icontains=query))

        serializer = MovieInfoSerializers(queryset, many=True)
        return Response(serializer.data)
