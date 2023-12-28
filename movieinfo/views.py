import json
import re
import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import utils
from .models import MovieInfo, OneLineCritic
from .permissions import OneLineCriticIsAuthorOrReadOnly
from accounts.models import User
from accounts.models import LikeMovie, WatchedMovie, WatchlistMovie

from .serializers import (
    MovieInfoSerializers,
    OneLineCriticSerializers,
    OneLineCriticSaveSerializers,
    OneLineCriticCreateUpdateSerializers,
    LikeMovieSerializers,
    WatchlistMovieSerializers,
    WatchedMovieSerializers,
)


class SearchMovieAPIView(APIView):
    def post(self, request):
        query = json.loads(request.body)["query"]
        query = re.sub(" ", "", query)
        res = utils.get_movie_info(query)

        if res.status_code == 200:
            data = res.data
            if data["Data"][0]["Count"] == 0:
                return Response({"message": "검색 결과가 없습니다."})
            utils.save_movie_info(data)

        queryset = MovieInfo.objects.filter(Q(searchTitle__icontains=query))
        serializer = MovieInfoSerializers(queryset, many=True)
        return Response(serializer.data)


class MovieInfoViewSet(viewsets.ModelViewSet):
    queryset = MovieInfo.objects.all()
    serializer_class = MovieInfoSerializers
    http_method_names = ["get"]  # allowed methods


class OneLineCriticViewSet(viewsets.ModelViewSet):
    queryset = OneLineCritic.objects.all()
    serializer_class = OneLineCriticSerializers
    permission_classes = [OneLineCriticIsAuthorOrReadOnly]
    http_method_names = ["get", "post", "delete", "patch"]

    def list(self, request, *args, **kwargs):
        pk = self.kwargs["movie_id"]
        queryset = OneLineCritic.objects.filter(movie__id=pk)
        serializer = OneLineCriticSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["author"] = User.objects.get(username=request.user).pk
        data["movie"] = self.kwargs["movie_id"]
        serializer = OneLineCriticSaveSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        create method에서 실제로 데이터베이스에 값을 저장하는 method.
        "url: /movieinfo/detail/<int:movie_id>/onelinecritic/"에서 'movie_id'를 통해,
        MovieInfo의 id == movie_id인 레코드를 OneLineCritic의 movie의 외래키로 연결시키도록 한다.
        이때 사용자로부터 movie에 대한 값은 받지 않으며, url을 통해서만 받는다.

        나머지 content와 starpoint의 값은 사용자가 입력한 값을 받는다.
        """
        req = self.request.data
        content = req["content"]
        starpoint = req["starpoint"]
        user = User.objects.get(id=req["author"])
        movie = MovieInfo.objects.get(id=self.kwargs["movie_id"])
        serializer.save(
            content=content,
            starpoint=starpoint,
            movie=movie,
            author=user,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        url예시: /movieinfo/detail/<int:movie_id>/onelinecritic/<int:pk>/
        model: OneLineCritic
        serializer: OneLineCriticSerializers

        현재 주소의 movie_id 값과 pk 값을 통해 OneLineCritic 모델의 movie==movie_id 이고,
        모델의 id==pk 인 항목을 objects.get을 통해 찾는다.
        해당 항목이 있다면 serializer를 통해 직렬화된 값을 응답,
        그렇지 않으면 400에러를 보낸다.
        """
        pk = self.kwargs["pk"]
        movie_id = self.kwargs["movie_id"]
        try:
            instance = OneLineCritic.objects.get(Q(id=pk) & Q(movie__id=movie_id))
            serializer = OneLineCriticSerializers(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            errorMessage = {"message": "잘못된 응답입니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        movie_id = self.kwargs["movie_id"]
        try:
            instance = OneLineCritic.objects.get(Q(id=pk) & Q(movie=movie_id))
            data = request.data
            data["user"] = request.user
            data["movie_id"] = movie_id
            serializer = OneLineCriticCreateUpdateSerializers(
                instance=instance, data=data
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            errorMessage = {"message": "잘못된 응답입니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        req = self.request.data
        content = req["content"]
        starpoint = req["starpoint"]
        serializer.save(
            content=content,
            starpoint=starpoint,
        )

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        movie_id = self.kwargs["movie_id"]

        try:
            instance = OneLineCritic.objects.get(Q(id=pk) & Q(movie=movie_id))
            if request.user != instance.author:
                raise ValueError
        except:
            errorMessage = {"message": "잘못된 응답입니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        message = {"message": "삭제되었습니다."}
        return Response(message, status=status.HTTP_204_NO_CONTENT)


class UserLWWViewSet(viewsets.ModelViewSet):
    """
    좋아요, 볼 영화, 본 영화를 체크할 수 있는 viewset

    """

    queryset = LikeMovie.objects.all()
    serializer_class = LikeMovieSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = "user"

    def list(self, request, *args, **kwargs):
        pk = self.kwargs["movie_id"]
        mode = kwargs["mode"]

        if mode == "like":
            queryset = LikeMovie.objects.filter(movie__id=pk)
            serializer = LikeMovieSerializers(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif mode == "watchlist":
            queryset = WatchlistMovie.objects.filter(movie__id=pk)
            serializer = WatchlistMovieSerializers(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif mode == "watched":
            queryset = WatchedMovie.objects.filter(movie__id=pk)
            serializer = WatchedMovieSerializers(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            errorMessage = {"message": "잘못된 응답입니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        movie_id = self.kwargs["movie_id"]
        user = self.kwargs["user"]
        mode = kwargs["mode"]

        if mode == "like":
            queryset = LikeMovie.objects.get(Q(movie__id=movie_id) & Q(user__pk=user))
            serializer = LikeMovieSerializers(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif mode == "watchlist":
            queryset = WatchlistMovie.objects.get(
                Q(movie__id=movie_id) & Q(user__pk=user)
            )
            serializer = WatchlistMovieSerializers(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif mode == "watched":
            queryset = WatchedMovie.objects.get(
                Q(movie__id=movie_id) & Q(user__pk=user)
            )
            serializer = WatchedMovieSerializers(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            errorMessage = {"message": "잘못된 응답입니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        movie_id = kwargs["movie_id"]
        mode = kwargs["mode"]
        user = request.user
        data = {"movie_id": movie_id, "user": user}
        if mode == "like":
            instance = LikeMovieSerializers(data=data)
            instance.is_valid(raise_exception=True)
            instance.save(
                movie=MovieInfo.objects.get(id=movie_id), user=self.request.user
            )
            return Response(instance.data, status=status.HTTP_201_CREATED)
        elif mode == "watchlist":
            instance = WatchlistMovieSerializers(data=data)
            instance.is_valid(raise_exception=True)
            instance.save(
                movie=MovieInfo.objects.get(id=movie_id), user=self.request.user
            )
            return Response(instance.data, status=status.HTTP_201_CREATED)
        elif mode == "watched":
            instance = WatchedMovieSerializers(data=data)
            instance.is_valid(raise_exception=True)
            instance.save(
                movie=MovieInfo.objects.get(id=movie_id), user=self.request.user
            )
            return Response(instance.data, status=status.HTTP_201_CREATED)
        else:
            errorMessage = {"message": "잘못된 응답입니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        movie_id = kwargs["movie_id"]
        mode = kwargs["mode"]
        user = User.objects.get(pk=kwargs["user"])
        if request.user == user:
            if mode == "like":
                try:
                    instance = LikeMovie.objects.get(
                        Q(user=user) & Q(movie=MovieInfo.objects.get(id=movie_id))
                    )
                    if user == instance.user:
                        instance.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        raise ValueError
                except:
                    errorMessage = {"message": "잘못된 응답입니다."}
                    return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
            elif mode == "watchlist":
                try:
                    instance = WatchlistMovie.objects.get(
                        Q(user=user) & Q(movie=MovieInfo.objects.get(id=movie_id))
                    )
                    if user == instance.user:
                        instance.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        raise ValueError
                except:
                    errorMessage = {"message": "잘못된 응답입니다."}
                    return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
            elif mode == "watched":
                try:
                    instance = WatchedMovie.objects.get(
                        Q(user=user) & Q(movie=MovieInfo.objects.get(id=movie_id))
                    )
                    if user == instance.user:
                        instance.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)
                    else:
                        raise ValueError
                except:
                    errorMessage = {"message": "잘못된 응답입니다."}
                    return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
        else:
            errorMessage = {"message": "권한이 없습니다."}
            return Response(errorMessage, status=status.HTTP_400_BAD_REQUEST)
