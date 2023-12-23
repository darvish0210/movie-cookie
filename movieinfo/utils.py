import json
import requests
import re

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from .models import MovieInfo, Actor, Director, Poster, Vod, Nation, Company, Genre


def get_movie_info(query):
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


def save_movie_info(data):
    for i in range(data["Data"][0]["Count"]):
        title = data["Data"][0]["Result"][i]["title"]
        title = re.sub(r" \!HS ", "", title)
        title = re.sub(r" \!HE ", "", title)
        title = re.sub(r"^\s+|\s+$", "", title)
        title = re.sub(r" +", " ", title)
        searchTitle = re.sub(r" ", "", title)
        docid = data["Data"][0]["Result"][i]["DOCID"]

        genres = data["Data"][0]["Result"][i]["genre"]
        if re.match(r"에로", genres):
            continue

        try:
            MovieInfo.objects.get(searchTitle=searchTitle)
        except:
            plot = ""
            for plotData in data["Data"][0]["Result"][i]["plots"]["plot"]:
                if plotData["plotLang"] == "한국어":
                    plot = plotData["plotText"]

            runtime = int(data["Data"][0]["Result"][i]["runtime"] or 0)

            rating = data["Data"][0]["Result"][i]["rating"]

            release_date = (
                f'{data["Data"][0]["Result"][i]["repRlsDate"][0:4]}-{data["Data"][0]["Result"][i]["repRlsDate"][4:6]}-{data["Data"][0]["Result"][i]["repRlsDate"][6:8]}'
                if data["Data"][0]["Result"][i]["repRlsDate"]
                else "1930-01-01"
            )

            new_data = MovieInfo(
                searchTitle=searchTitle,
                docid=docid,
                title=title,
                plot=plot,
                runtime=runtime,
                rating=rating,
                release_date=release_date,
            )
            new_data.save()

            for director in data["Data"][0]["Result"][i]["directors"]["director"]:
                name = director["directorNm"]
                number = director["directorId"]
                if name and number:
                    try:
                        db_director = Director(name=name, number=number)
                        db_director.save()
                        new_data.directors.add(db_director)
                    except:
                        db_director = Director.objects.get(number=number)
                        new_data.directors.add(db_director)

            posters = str(data["Data"][0]["Result"][i]["posters"]).split("|")
            for poster in posters:
                if poster:
                    db_poster = Poster(url=poster)
                    db_poster.save()
                    new_data.posters.add(db_poster)

            for vod in data["Data"][0]["Result"][i]["vods"]["vod"]:
                title = vod["vodClass"]
                url = re.sub(r"trailerPlayPop\?pFileNm=", "play/", vod["vodUrl"])
                if title and url:
                    db_vod = Vod(title=title, url=url)
                    db_vod.save()
                    new_data.vods.add(db_vod)

            for actor in data["Data"][0]["Result"][i]["actors"]["actor"]:
                name = actor["actorNm"]
                number = actor["actorId"]
                if name and number:
                    try:
                        db_actor = Actor(name=name, number=number)
                        db_actor.save()
                        new_data.actors.add(db_actor)
                    except:
                        db_actor = Actor.objects.get(number=number)
                        new_data.actors.add(db_actor)

            nations = re.split(", *", data["Data"][0]["Result"][i]["nation"])
            for nation in nations:
                if nation:
                    try:
                        db_nation = Nation(name=nation)
                        db_nation.save()
                        new_data.nations.add(db_nation)
                    except:
                        db_nation = Nation.objects.get(name=nation)
                        new_data.nations.add(db_nation)

            companies = re.split(", *", data["Data"][0]["Result"][i]["company"])
            for company in companies:
                if company:
                    try:
                        db_company = Company(name=company)
                        db_company.save()
                        new_data.companies.add(db_company)
                    except:
                        db_company = Company.objects.get(name=company)
                        new_data.companies.add(db_company)

            genres = re.split(", *", genres)
            for genre in genres:
                if genre:
                    try:
                        db_genre = Genre(genre=genre)
                        db_genre.save()
                        new_data.genres.add(db_genre)
                    except:
                        db_genre = Genre.objects.get(genre=genre)
                        new_data.genres.add(db_genre)
