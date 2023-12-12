import json
import requests
import re

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from .models import MovieInfo


def getMovieInfo(query):
    KMDB_API_KEY = str(settings.KMDB_API_KEY)
    url = f"https://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={KMDB_API_KEY}&detail=Y&title={query}&listCount=100"
    print(url)
    res = requests.get(url)
    if res.status_code == 200:
        response_body = res.content
        dict = json.loads(response_body.decode("utf-8"))
        return Response(dict, status=status.HTTP_200_OK)
    else:
        return Response(res.status_code, status=status.HTTP_400_BAD_REQUEST)


def saveMovieInfo(data):
    for i in range(data["Data"][0]["Count"]):
        title = data["Data"][0]["Result"][i]["title"]
        title = re.sub(r" \!HS ", "", title)
        title = re.sub(r" \!HE ", "", title)
        title = re.sub(r"^\s+|\s+$", "", title)
        title = re.sub(r" +", " ", title)
        searchTitle = re.sub(r" ", "", title)

        try:
            MovieInfo.objects.get(searchTitle=searchTitle)
        except:
            directors = []
            for director in data["Data"][0]["Result"][i]["directors"]["director"]:
                directors.append(director["directorNm"])
            directors = "|".join(directors)

            if not directors:
                continue

            posters = data["Data"][0]["Result"][i]["posters"]  # poster 분리 처리
            vods = []
            for vod in data["Data"][0]["Result"][i]["vods"]["vod"]:
                vods.append(json.dumps(vod, ensure_ascii=False))
            vods = "|".join(vods)
            actors = []
            for actor in data["Data"][0]["Result"][i]["actors"]["actor"]:
                actors.append(actor["actorNm"])
            actors = "|".join(actors)
            nations = data["Data"][0]["Result"][i]["nation"]
            nations = re.sub(", *", "|", nations)
            companies = data["Data"][0]["Result"][i]["company"]
            companies = re.sub(", *", "|", companies)
            plot = ""
            for plotData in data["Data"][0]["Result"][i]["plots"]["plot"]:
                if plotData["plotLang"] == "한국어":
                    plot = plotData["plotText"]
            runtime = int(data["Data"][0]["Result"][i]["runtime"] or 0)
            rating = data["Data"][0]["Result"][i]["rating"]
            genres = data["Data"][0]["Result"][i]["genre"]
            genres = re.sub(", *", "|", genres)

            if re.match(r"에로", genres):
                continue

            releaseDate = (
                str(data["Data"][0]["Result"][i]["repRlsDate"])
                if data["Data"][0]["Result"][i]["repRlsDate"]
                else "1930-01-01"
            )

            newData = MovieInfo(
                title=title,
                searchTitle=searchTitle,
                posters=posters,
                vods=vods,
                directors=directors,
                actors=actors,
                nations=nations,
                companies=companies,
                plot=plot,
                runtime=runtime,
                rating=rating,
                genres=genres,
                releaseDate=releaseDate,
            )
            newData.save()
