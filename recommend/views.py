# recommend/views.py
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Recommend
from .permissions import RecommendPermission
from .serializers import RecommendSerializer
from .schema_examples import (
    GENERATE_REQUEST,
    GENERATE_RESPONSE,
    RECOMMEND_REQUEST,
    RECOMMEND_RESPONSE,
    RECOMMEND_LIST,
)
from movieinfo.models import MovieInfo, Poster
from movieinfo.serializers import MovieInfoSerializers
from movieinfo.utils import save_movie_info

import json
import requests
import pandas as pd


@extend_schema_view(
    generate=extend_schema(  # POST recommend/generate/
        description="입력값을 토대로 영화를 추천해줍니다. `input_nation`으로 국내, 해외 여부를 입력하고, `input_period`로 2000년대, 2010년대, 2020년대 중 원하는 기간을 입력하고, `input_genre`로 원하는 장르를 입력하면 됩니다. 중복 가능하고, 여러가지를 입력하고 싶으면 `|`로 구분하여 입력하면 됩니다. 그럼 누적관객수 순으로 정렬된 영화 추천 리스트 중에서 영화를 하나 추천해줍니다. **로그인 없이도 이용 가능**하고, **로그인을 하면 본인의 선호장르 태그와 좋아요한 영화도 반영**되어 더욱 본인의 취향에 맞게 추천받을 수 있습니다.",
        request=RecommendSerializer,
        responses={200: RecommendSerializer},
        examples=[GENERATE_REQUEST, GENERATE_RESPONSE],
    ),
    list=extend_schema(  # GET recommend/
        description="요청을 보낸 유저가 저장한 **추천객체들을 전부 가져옵니다.** 추천객체에는 본인이 입력했던 값들과 그것을 이용하여 추천해준 영화가 담겨있습니다. **로그인을 한 유저만 이용 가능**합니다.",
        request=RecommendSerializer,
        responses={200: RecommendSerializer},
        examples=[RECOMMEND_LIST],
    ),
    create=extend_schema(  # POST recommend/
        description="**추천받은 값을 저장**합니다. `recommend/generate/`에서 사용한 `input_nation`, `input_period`, `input_genre`, 그리고 추천받은 영화의 `영화정보객체 id값`을 입력합니다. 그럼 데이터베이스에 저장이 되어, 나중에도 추천받았던 영화들을 볼 수 있습니다. **로그인을 한 유저만 이용 가능**합니다.",
        request=RecommendSerializer,
        responses={201: RecommendSerializer},
        examples=[RECOMMEND_REQUEST, RECOMMEND_RESPONSE],
    ),
    retrieve=extend_schema(  # GET recommend/<id>/
        description="`id`를 이용해서 해당 추천영화 정보를 가져옵니다. **로그인을 한 유저가 본인의 추천영화만** 가져올 수 있습니다.",
        request=RecommendSerializer,
        responses={200: RecommendSerializer},
        examples=[RECOMMEND_RESPONSE],
    ),
    partial_update=extend_schema(  # PATCH recommend/<id>/
        description="`id`를 이용해서 해당 추천영화 객체에 수정된 입력값으로 재추천받은 새로운 영화정보를 업데이트합니다. 전체 수정이 아닌 부분만 수정이 되므로 `PUT`대신 `PATCH`를 이용합니다. **로그인을 한 유저가 본인의 추천영화만 수정**할 수 있습니다.",
        request=RecommendSerializer,
        responses={200: RecommendSerializer},
        examples=[RECOMMEND_REQUEST, RECOMMEND_RESPONSE],
    ),
    destroy=extend_schema(  # DELETE recommend/<id>/
        description="`id`를 이용해서 해당 추천영화 정보를 삭제합니다. **로그인을 한 유저가 본인의 추천영화만 삭제**할 수 있습니다.",
        request=RecommendSerializer,
        responses={204: RecommendSerializer},
    ),
    update=extend_schema(deprecated=True, exclude=True),
)
class RecommendViewSet(ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer
    permission_classes = [RecommendPermission]

    def get_queryset(self):
        """
        이 함수는 요청 보내는 유저의 추천객체만 조회하기 위해 필터링하는 역할을 합니다.
        """
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        """
        이 함수는 추천객체를 저장할 때 호출되는 `create` 함수에서 객체에 저장하는 역할을 하는데, `serializer`에 유저 정보와 영화 정보를 같이 저장해줍니다.\n
        유저 정보가 필요하므로 로그인 된 유저만 이용 가능합니다.\n
        (비로그인 유저는 이 함수 대신 프론트엔드에서 로컬 스토리지에 임시로 저장합니다.)
        """
        movie_id = serializer.validated_data.get("movie_id")
        user = self.request.user
        movie = MovieInfo.objects.get(id=movie_id)
        serializer.save(user=user, movie=movie)

    def perform_update(self, serializer):
        """
        이 함수는 추천객체를 수정할 때 호출되는 `partial_update` 함수에서 객체에 수정된 데이터를 저장하는 역할을 하는데, `serializer`에 영화 정보를 같이 저장해줍니다.\n
        로그인을 한 유저가 본인의 추천객체만 수정할 수 있습니다.
        """
        movie_id = serializer.validated_data.get("movie_id")
        movie = MovieInfo.objects.get(id=movie_id)
        serializer.save(movie=movie)

    @action(detail=False, methods=["POST", "GET"])
    def generate(self, request):
        """
        이 함수는 추천 영화를 생성하는 함수입니다.\n
        로그인 여부에 상관 없이 이용 가능하고 `POST`요청만 받습니다.\n
        입력값들로 필터링 된 `추천영화 리스트`를 가져와서,
        유저가 로그인 되어있을 경우엔 유저의 선호에 따른 `가중치` 값을 추가하고,
        `가중치`가 높은 순, `누적관객수`가 높은 순으로 리스트를 정렬합니다.\n
        정렬 후, 상위 10개의 영화 중 하나를 랜덤으로 골라 추천해줍니다.
        """
        serializer = RecommendSerializer(data=request.data)
        if serializer.is_valid():
            # 입력값으로 필터링 된 영화 리스트 받아오기
            genre = serializer.validated_data.get("genre")
            nation_korean = serializer.validated_data.get("nation_korean")
            nation_foreign = serializer.validated_data.get("nation_foreign")
            period_2000 = serializer.validated_data.get("period_2000")
            period_2010 = serializer.validated_data.get("period_2010")
            period_2020 = serializer.validated_data.get("period_2020")
            selected_movies = self.get_movie_list(
                genre,
                nation_korean,
                nation_foreign,
                period_2000,
                period_2010,
                period_2020,
            )
            if isinstance(selected_movies, Response):
                return selected_movies

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
            if not movie.data["docid"]:
                return Response({"detail": "KMDB API 에러입니다. 나중에 시도해주세요."}, status=400)
            if movie.data["posters"][0]:
                poster_id = movie.data["posters"][0]["id"]
                poster_url = Poster.objects.get(id=poster_id).url
            else:
                poster_url = None

            # 모델 형식에 맞게 리턴
            recommended_data = {
                "genre": [g.genre for g in genre],
                "nation_korean": nation_korean,
                "nation_foreign": nation_foreign,
                "period_2000": period_2000,
                "period_2010": period_2010,
                "period_2020": period_2020,
                "movie_id": movie.data["id"],
                "movie_title": movie.data["title"],
                "poster_url": poster_url,
            }
            return Response(recommended_data)
        else:
            return Response(serializer.errors, status=400)

    @staticmethod
    def get_movie_list(
        genres,
        nation_korean,
        nation_foreign,
        period_2000,
        period_2010,
        period_2020,
    ):
        """
        이 함수는 입력값으로 추천영화 csv파일을 필터링해서 리턴해주는 함수입니다.\n
        먼저, 불리언값인 `nation_korean`, `nation_foreign`값을 통해 `True` 여부에 따라 국내영화, 해외영화 `csv`파일을 불러옵니다.\n
        그 다음, 불리언값인 `period_2000`, `period_2010`, `period_2020`값을 통해 `2000년대`, `2010년대`, `2020년대` 중 `True`인 시대에 개봉한 영화들을 필터링합니다.\n
        마지막으로 `genres`를 통해 유저가 입력한 장르를 하나라도 포함하는 영화만 필터링합니다.\n
        세 가지 필터링 모두 `중복 선택이 가능`합니다.\n
        필터링 후, 중복을 제거하고 미리 가중치 컬럼을 생성한 후 리턴합니다.
        """
        # nation - 국내, 해외 여부에 따라 CSV 파일 추가
        movies_data = pd.DataFrame()
        if nation_korean:
            movies_data = pd.concat([movies_data, pd.read_csv("static/korean.csv")])
        if nation_foreign:
            movies_data = pd.concat([movies_data, pd.read_csv("static/foreign.csv")])
        if movies_data.empty:
            return Response({"detail": "하나 이상의 국가를 선택해주세요."}, status=400)

        # period - 개봉연도 조건에 따른 필터링
        movies_period = pd.DataFrame()
        if period_2000:
            movies_period = pd.concat(
                [movies_period, movies_data[movies_data["개봉연도"] < 2010]]
            )
        if period_2010:
            movies_period = pd.concat(
                [
                    movies_period,
                    movies_data[
                        (movies_data["개봉연도"] >= 2010) & (movies_data["개봉연도"] < 2020)
                    ],
                ]
            )
        if period_2020:
            movies_period = pd.concat(
                [movies_period, movies_data[movies_data["개봉연도"] >= 2020]]
            )
        movies_data = movies_period
        if movies_data.empty:
            return Response({"detail": "하나 이상의 시대를 선택해주세요."}, status=400)

        # genres - 장르 조건에 따른 필터링
        movies_list = pd.DataFrame()
        for genre in genres:
            genre = genre.genre
            movies_list = pd.concat(
                [
                    movies_list,
                    movies_data[movies_data["kmdb장르"].str.contains(genre)],
                ]
            )
        if movies_list.empty:
            return Response({"detail": "하나 이상의 장르를 선택해주세요."}, status=400)

        # 중복 제거, 가중치 컬럼 생성
        movies_list = movies_list.drop_duplicates(subset="번호")
        movies_list["가중치"] = 0
        return movies_list

    @staticmethod
    def update_weight(user, movie_list):
        """
        로그인을 한 유저의 경우, 유저의 `선호장르`, `좋아요한 영화`에 따른 `가중치`를 이 함수를 통해 부여할 수 있습니다.\n
        추천영화 리스트의 각 영화들에 대해서, 그 영화의 장르에 유저가 선호하는 장르가 포함되어 있다면 그 영화는 `+3`의 가중치를 얻습니다.\n
        또한 그 영화의 장르에 유저가 좋아요를 누른 영화들의 장르가 포함되어 있다면 그 영화는 `+1`의 가중치를 얻습니다.\n
        유저가 좋아요를 누른 영화들의 장르보다 직접 선호를 표시한 장르가 좀 더 유저의 취향에 맞으므로 높은 가중치를 갖도록 설정하였습니다.
        """
        # 선호장르태그 - user의 genre로 연결
        user_genres = user.genre.all() if user.genre.all() else []
        # 좋아요한 영화 - LikeMovie의 user의 related name
        user_liked_movies = user.likes.all() if user.likes.all() else []

        # 선호장르 가중치 부여
        for genre in user_genres:
            movie_list.loc[movie_list["kmdb장르"].str.contains(genre.genre), "가중치"] += 3

        # 영화 좋아요에 따른 가중치 부여
        for liked_movie in user_liked_movies:
            # user로 필터링된 LikeMovie모델 - 영화 - 장르
            liked_genre = liked_movie.movie.genres.split("|")
            for genre in liked_genre:
                movie_list.loc[
                    movie_list["kmdb장르"].str.contains(genre.genre), "가중치"
                ] += 1

        return movie_list

    @staticmethod
    def get_movieinfo(movie_row):
        """
        이 함수는 추천된 영화의 영화정보를 가져오는 함수입니다.\n
        기존 데이터베이스에 있는지 확인을 먼저 하고, 없으면 `KMDB API`로 요청을 보내서 응답받은 영화의 정보를 `MovieInfo`객체에 저장합니다.\n
        그 후 추천된 영화에 대한 `MovieInfo` 정보를 리턴합니다.
        """
        movie_id = movie_row.iloc[0]["movie_id"]
        movie_seq = str(movie_row.iloc[0]["movie_seq"]).zfill(5)
        docid = movie_id + movie_seq
        movie_info = MovieInfo.objects.filter(docid=docid).first()
        # 기존 DB에 없을 경우 새로 요청 후 저장하고 불러옴
        if not movie_info:
            # 영화 정보 KMDB API 요청
            KMDB_API_KEY = str(settings.KMDB_API_KEY)
            url = f"https://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={KMDB_API_KEY}&detail=Y&listCount=1&movieId={movie_id}&movieSeq={movie_seq}"
            res = requests.get(url)
            if res.status_code == 200:
                response_body = res.content
                data = json.loads(response_body.decode("utf-8"))
                save_movie_info(data)
                movie_info = MovieInfo.objects.filter(docid=docid).first()
            else:
                return None
        movie = MovieInfoSerializers(movie_info)
        return movie
