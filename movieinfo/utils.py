import json
import requests
import re
from datetime import datetime


# import django

# django.setup()

from django.db import connections
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


def save_movie_info(datas):
    for i in range(datas["Data"][0]["Count"]):
        data = datas["Data"][0]["Result"][i]
        title = data["title"]
        title = re.sub(r" \!HS ", "", title)
        title = re.sub(r" \!HE ", "", title)
        title = re.sub(r"^\s+|\s+$", "", title)
        title = re.sub(r" +", " ", title)
        searchTitle = re.sub(r" ", "", title)
        docid = data["DOCID"]

        genres = data["genre"]

        if re.match(r"에로", genres):
            # 특정 장르 검색 방지
            continue

        try:
            MovieInfo.objects.get(searchTitle=searchTitle)
        except:
            plot = ""
            for plotData in data["plots"]["plot"]:
                if plotData["plotLang"] == "한국어":
                    plot = plotData["plotText"]

            runtime = int(data["runtime"] or 0)

            rating = data["rating"]

            release_date = (
                f'{data["repRlsDate"][0:4]}-{data["repRlsDate"][4:6]}-{data["repRlsDate"][6:8]}'
                if data["repRlsDate"]
                else "1930-01-01"
            )

            try:
                bool(datetime.strptime(release_date, "%Y-%m-%d"))
            except ValueError:
                release_date = "1930-01-01"

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

            save_directors(data, new_data)
            save_postsers(data, new_data)
            save_vods(data, new_data)
            save_actors(data, new_data)
            save_nations(data, new_data)
            save_companies(data, new_data)
            save_genres(genres, new_data)


def save_directors(data, new_data):
    for director in data["directors"]["director"]:
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


def save_postsers(data, new_data):
    posters = str(data["posters"]).split("|")
    for poster in posters:
        if poster:
            db_poster = Poster(url=poster)
            db_poster.save()
            new_data.posters.add(db_poster)


def save_vods(data, new_data):
    for vod in data["vods"]["vod"]:
        title = vod["vodClass"]
        url = re.sub(r"trailerPlayPop\?pFileNm\=", "play/", vod["vodUrl"])
        if title and url:
            db_vod = Vod(title=title, url=url)
            db_vod.save()
            new_data.vods.add(db_vod)


def save_actors(data, new_data):
    for actor in data["actors"]["actor"]:
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


def save_nations(data, new_data):
    nations = re.split(", *", data["nation"])
    for nation in nations:
        if nation:
            try:
                db_nation = Nation(name=nation)
                db_nation.save()
                new_data.nations.add(db_nation)
            except:
                db_nation = Nation.objects.get(name=nation)
                new_data.nations.add(db_nation)


def save_companies(data, new_data):
    companies = re.split(", *", data["company"])
    for company in companies:
        if company:
            try:
                db_company = Company(name=company)
                db_company.save()
                new_data.companies.add(db_company)
            except:
                db_company = Company.objects.get(name=company)
                new_data.companies.add(db_company)


def save_genres(genres, new_data):
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
