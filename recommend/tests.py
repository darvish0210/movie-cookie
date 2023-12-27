# recommend/tests.py
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Recommend
from accounts.models import User
from movieinfo.models import Genre, MovieInfo, Poster


class RecommendAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        테스트 데이터를 생성합니다.\n
        영화추천의 경우 상위 10개중 무작위로 하나를 고르기 때문에 해당 입력값에 대한 상위 10개 영화객체를 생성하였습니다.\n
        `cls.update_movie` 객체는 수정 테스트를 위해 생성하였습니다.\n
        `cls.recommend` 객체는 목록 조회, 수정, 삭제 테스트를 위해 생성하였습니다.
        """
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.genre1 = Genre.objects.create(genre="시대극/사극")
        cls.genre2 = Genre.objects.create(genre="액션")
        cls.genre3 = Genre.objects.create(genre="전기")
        cls.genre4 = Genre.objects.create(genre="SF")
        cls.genre5 = Genre.objects.create(genre="어드벤처")
        cls.poster1 = Poster.objects.create(url="test1.jpg")
        cls.poster2 = Poster.objects.create(url="test2.jpg")
        title_list = [
            "명량",
            "베테랑",
            "도둑들",
            "암살",
            "광해, 왕이 된 남자",
            "부산행",
            "검사외전",
            "엑시트",
            "관상",
            "설국열차",
        ]
        docid_list = [
            "K13963",
            "K14173",
            "K13031",
            "K14409",
            "K13229",
            "K14687",
            "K15172",
            "K20773",
            "K13400",
            "K13349",
        ]
        for i in range(10):
            cls.movieinfo = MovieInfo.objects.create(
                title=title_list[i],
                searchTitle=title_list[i],
                docid=docid_list[i],
            )
            cls.movieinfo.posters.set([cls.poster1])
        cls.update_movie = MovieInfo.objects.create(
            title="아바타",
            searchTitle="아바타",
            docid="F24464",
        )
        cls.update_movie.posters.set([cls.poster2])
        cls.recommend = Recommend.objects.create(
            user=cls.user,
            nation_korean=True,
            nation_foreign=False,
            period_2000=False,
            period_2010=False,
            period_2020=True,
            movie=cls.movieinfo,
            movie_title=cls.movieinfo.title,
            poster_url="http://example.com/poster.jpg",
        )
        cls.recommend.genre.set([cls.genre1, cls.genre2, cls.genre3])

    def test_generate_authenticated(self):
        """
        로그인 한 유저에 대해 영화추천 요청을 테스트합니다.\n
        응답 값에 기존 입력값이 같은지, 새롭게 추가된 값들이 있는지 확인합니다.
        """
        url = "/recommend/generate/"
        self.client.force_authenticate(user=self.user)
        data = {
            "genre": ["시대극/사극", "액션", "전기"],
            "nation_korean": True,
            "nation_foreign": False,
            "period_2000": False,
            "period_2010": True,
            "period_2020": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response["genre"], ["시대극/사극", "액션", "전기"])
        self.assertEqual(response["nation_korean"], True)
        self.assertEqual(response["period_2000"], False)
        self.assertIn("movie_id", response)
        self.assertIn("movie_title", response)
        self.assertIn("poster_url", response)

    def test_generate_unauthenticated(self):
        """
        로그인 하지 않은 유저에 대해 영화추천 요청을 테스트합니다.\n
        응답 값에 기존 입력값이 같은지, 새롭게 추가된 값들이 있는지 확인합니다.
        """
        url = "/recommend/generate/"
        self.client.force_authenticate(user=None)
        data = {
            "genre": ["시대극/사극", "액션", "전기"],
            "nation_korean": True,
            "nation_foreign": False,
            "period_2000": False,
            "period_2010": True,
            "period_2020": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response["genre"], ["시대극/사극", "액션", "전기"])
        self.assertEqual(response["nation_korean"], True)
        self.assertEqual(response["period_2000"], False)
        self.assertIn("movie_id", response)
        self.assertIn("movie_title", response)
        self.assertIn("poster_url", response)

    def test_generate_invalid_data(self):
        """
        입력 값이 잘못된 데이터를 포함하고 있을 경우를 테스트합니다.\n
        상태코드를 확인하고, 잘못 입력된 부분에 대한 에러메세지가 있는지 확인합니다.
        """
        url = "/recommend/generate/"
        self.client.force_authenticate(user=None)
        data = {
            "genre": "판타지, 가족, 드라마",
            "nation_korean": True,
            "nation_foreign": "",
            "period_2000": False,
            "period_2010": [],
            "period_2020": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = response.json()
        self.assertIn("genre", response)
        self.assertIn("nation_foreign", response)
        self.assertIn("period_2010", response)

    def test_create_authenticated(self):
        """
        로그인 한 유저에 대해 영화추천객체 생성을 테스트합니다.\n
        응답 값에 새로 추가된 값들이 있는지 확인합니다.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "genre": ["시대극/사극", "액션", "전기"],
            "nation_korean": True,
            "nation_foreign": False,
            "period_2000": False,
            "period_2010": True,
            "period_2020": False,
            "movie_id": self.movieinfo.id,
            "movie_title": self.movieinfo.title,
            "poster_url": "http://example.com/poster2.jpg",
        }
        response = self.client.post("/recommend/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = response.json()
        self.assertIn("id", response)
        self.assertIn("user", response)
        self.assertIn("movie", response)
        self.assertIn("created_at", response)

    def test_create_unauthenticated(self):
        """
        로그인 하지 않은 유저에 대해 영화추천객체 저장을 테스트합니다.\n
        로그인을 하지 않으면 저장되지 않는지 확인합니다.
        """
        self.client.force_authenticate(user=None)
        data = {
            "genre": ["시대극/사극", "액션", "전기"],
            "nation_korean": True,
            "nation_foreign": False,
            "period_2000": False,
            "period_2010": True,
            "period_2020": False,
            "movie_id": self.movieinfo.id,
            "movie_title": self.movieinfo.title,
            "poster_url": "http://example.com/poster2.jpg",
        }
        response = self.client.post("/recommend/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = response.json()
        self.assertIn("detail", response)

    def test_list(self):
        """
        로그인 한 유저에 대해 추천영화 목록 요청을 테스트합니다.\n
        처음 생성했던 1개의 객체가 목록에 있는지 확인합니다.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/recommend/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(len(response), 1)

    def test_retrieve(self):
        """
        로그인 한 유저에 대해 추천영화 객체 조회 요청을 테스트합니다.\n
        처음 생성했던 1개의 객체가 잘 요청되는지, 필드들이 존재하는지 확인합니다.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/recommend/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertIn("id", response)
        self.assertIn("user", response)
        self.assertIn("genre", response)
        self.assertIn("nation_foreign", response)
        self.assertIn("period_2010", response)
        self.assertIn("movie", response)
        self.assertIn("created_at", response)

    def test_update(self):
        """
        로그인 한 유저에 대해 추천영화 수정 요청을 테스트합니다.\n
        기존의 추천객체 수정 후 수정된 값이 반영되었는지 확인합니다.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "genre": ["액션", "SF", "어드벤처"],
            "nation_korean": False,
            "nation_foreign": True,
            "period_2000": True,
            "period_2010": True,
            "period_2020": False,
            "movie_id": self.update_movie.id,
            "movie_title": self.update_movie.title,
            "poster_url": "http://example.com/poster.jpg",
        }
        response = self.client.patch("/recommend/1/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response["genre"], ["액션", "SF", "어드벤처"])
        self.assertEqual(response["nation_korean"], False)
        self.assertEqual(response["period_2000"], True)
        self.assertEqual(response["movie_title"], self.update_movie.title)

    def test_destroy(self):
        """
        로그인 한 유저에 대해 추천영화 삭제 요청을 테스트합니다.\n
        1개의 객체 삭제 후 목록조회를 했을 때 0개가 되었는지 확인합니다.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete("/recommend/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response2 = self.client.get("/recommend/")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response2 = response2.json()
        self.assertEqual(len(response2), 0)
