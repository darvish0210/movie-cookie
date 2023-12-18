# recommend/views.py
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Recommend
from .permissions import RecommendPermission
from .serializers import RecommendSerializer
from movieinfo.models import MovieInfo
from movieinfo.serializers import MovieInfoSerializers
from movieinfo.utils import saveMovieInfo

import json
import requests
import pandas as pd


class RecommendViewSet(ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer
    permission_classes = [RecommendPermission]

    # 해당 유저의 객체만 조회
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    # 추천객체 저장 시 유저, 영화 추가
    def perform_create(self, serializer):
        movie_id = serializer.validated_data.get("movie_id")
        user = self.request.user
        movie = MovieInfo.objects.get(id=movie_id)
        serializer.save(user=user, movie=movie)

    # 추천객체 수정 시 새로운 추천영화로 변경
    def perform_update(self, serializer):
        movie_id = serializer.validated_data.get("movie_id")
        movie = MovieInfo.objects.get(id=movie_id)
        serializer.save(movie=movie)

    # 추천 영화 생성하는 함수
    @action(detail=False, methods=["POST", "GET"])
    def generate(self, request):
        # 포스트 폼 보내기위한 테스트용 (나중에 삭제예정)
        if request.method == "GET":
            return Response({"message": "Generate GET"}, status=200)

        serializer = RecommendSerializer(data=request.data)
        if serializer.is_valid():
            # 입력값으로 필터링 된 영화 리스트 받아오기
            input_nation = serializer.validated_data.get("input_nation")
            input_period = serializer.validated_data.get("input_period")
            input_genre = serializer.validated_data.get("input_genre")
            selected_movies = self.get_movie_list(
                input_nation, input_period, input_genre
            )

            # 유저가 로그인한 경우 선호 장르와 좋아요한 영화 정보로 가중치 높이기
            if request.user.is_authenticated:
                user = request.user
                selected_movies = self.update_weight(user, selected_movies)

            # 가중치, 관객수 기준으로 내림차순 정렬
            selected_movies = selected_movies.sort_values(
                by=["가중치", "관객수"], ascending=[False, False]
            )

            # 상위 10개 중 랜덤으로 하나의 영화 선택 -> 그 영화정보 불러오기
            top_10 = selected_movies.head(10)
            pick = top_10.sample(n=1)
            movie = self.get_movieinfo(pick)

            # 모델 형식에 맞게 리턴
            recommended_data = {
                "input_nation": input_nation,
                "input_period": input_period,
                "input_genre": input_genre,
                "movie_id": movie.data["id"],
                "movie": movie.data,
            }
            return Response(recommended_data)
        else:
            return Response(serializer.errors, status=400)

    # 입력값으로 추천영화 csv파일을 필터링해서 리턴
    @staticmethod
    def get_movie_list(nation, period, genres):
        # nation - 국내, 해외, 국내|해외 여부에 따라 CSV 파일 선택
        if "국내" in nation and "해외" in nation:
            korean_data = pd.read_csv("static/korean.csv")
            foreign_data = pd.read_csv("static/foreign.csv")
            movies_data = pd.concat([korean_data, foreign_data])
        elif "국내" in nation:
            movies_data = pd.read_csv("static/korean.csv")
        elif "해외" in nation:
            movies_data = pd.read_csv("static/foreign.csv")
        else:
            return Response({"message": "Invalid input_nation value"}, status=400)

        # period - 개봉연도 조건에 따른 필터링
        movies = pd.DataFrame()
        if "2000년대" in period:
            movies = pd.concat([movies, movies_data[movies_data["개봉연도"] < 2010]])
        if "2010년대" in period:
            movies = pd.concat(
                [
                    movies,
                    movies_data[
                        (movies_data["개봉연도"] >= 2010) & (movies_data["개봉연도"] < 2020)
                    ],
                ]
            )
        if "2020년대" in period:
            movies = pd.concat([movies, movies_data[movies_data["개봉연도"] >= 2020]])
        movies_data = movies
        if movies_data.empty:
            return Response({"message": "Invalid input_period value"}, status=400)

        # genres - 장르를 |로 나눠서 영화 필터링
        movie_list = pd.DataFrame()
        for genre in genres.split("|"):
            movie_list = pd.concat(
                [
                    movie_list,
                    movies_data[movies_data["kmdb장르"].str.contains(genre)],
                ]
            )
        if movie_list.empty:
            return Response({"message": "Invalid input_genre value"}, status=400)

        # 중복 제거, 가중치 컬럼 생성
        movie_list = movie_list.drop_duplicates(subset="번호")
        movie_list["가중치"] = 0
        return movie_list

    # 유저의 선호장르태그, 좋아요한 영화에 따른 가중치 부여
    @staticmethod
    def update_weight(user, movie_list):
        # accounts 모델 내용에 따라 달라질 예정
        # 선호장르태그 - 일단 profile의 tag로 연결
        user_genres = user.profile.tag.split("|") if user.profile.tag else []
        # 좋아요한 영화 - LikeMovie의 user의 related name (수정예정)
        user_liked_movies = user.like.all()

        # 선호장르 가중치 부여
        for genre in user_genres:
            movie_list.loc[movie_list["kmdb장르"].str.contains(genre), "가중치"] += 3

        # 영화 좋아요에 따른 가중치 부여
        for liked_movie in user_liked_movies:
            # user로 필터링된 LikeMovie모델 - 영화 - 장르
            liked_genre = liked_movie.movie.genres.split("|")
            for genre in liked_genre:
                movie_list.loc[movie_list["kmdb장르"].str.contains(genre), "가중치"] += 1

        return movie_list

    # 영화정보 객체 받아오기
    @staticmethod
    def get_movieinfo(movie_column):
        movie_title = movie_column.iloc[0]["kmdb제목"]
        movie_genres = movie_column.iloc[0]["kmdb장르"]
        movie_id = movie_column.iloc[0]["movie_id"]
        movie_seq = str(movie_column.iloc[0]["movie_seq"]).zfill(5)

        movie_info = MovieInfo.objects.filter(
            title=movie_title, genres=movie_genres
        ).first()
        if not movie_info:  # 기존 DB에 없을 경우 새로 요청 후 저장하고 불러옴
            # 영화 정보 KMDB API 요청
            KMDB_API_KEY = str(settings.KMDB_API_KEY)
            url = f"https://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={KMDB_API_KEY}&detail=Y&listCount=1&movieId={movie_id}&movieSeq={movie_seq}"
            res = requests.get(url)
            if res.status_code == 200:
                response_body = res.content
                data = json.loads(response_body.decode("utf-8"))
                saveMovieInfo(data)
                movie_info = MovieInfo.objects.filter(title=movie_title).first()
            else:
                return Response({"message": "KMDB Error"}, status=400)
        movie = MovieInfoSerializers(movie_info)
        return movie
