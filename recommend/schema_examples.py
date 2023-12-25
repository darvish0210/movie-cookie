from drf_spectacular.utils import OpenApiExample

GENERATE_REQUEST = OpenApiExample(
    request_only=True,
    name="영화 추천 받기",
    value={
        "genre": ["판타지", "가족", "드라마"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
    },
)

GENERATE_RESPONSE = OpenApiExample(
    name="추천된 영화",
    response_only=True,
    value={
        "genre": ["판타지", "가족", "드라마"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
        "movie_id": 4,
        "movie_title": "알라딘",
        "poster_url": "http://file.koreafilm.or.kr/thm/02/00/05/16/tn_DPF018168.jpg",
    },
)

RECOMMEND_REQUEST = OpenApiExample(
    name="추천된 영화",
    request_only=True,
    value={
        "genre": ["판타지", "가족", "드라마"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
        "movie_id": 4,
        "movie_title": "알라딘",
        "poster_url": "http://file.koreafilm.or.kr/thm/02/00/05/16/tn_DPF018168.jpg",
    },
)

RECOMMEND_RESPONSE = OpenApiExample(
    response_only=True,
    name="저장/수정된 추천영화",
    value={
        "id": 1,
        "user": 1,
        "genre": ["가족", "드라마", "판타지"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
        "movie_id": 4,
        "movie_title": "알라딘",
        "poster_url": "http://file.koreafilm.or.kr/thm/02/00/05/16/tn_DPF018168.jpg",
        "movie": 4,
        "created_at": "2023-12-21T16:09:51.471721+09:00",
    },
)

RECOMMEND_LIST = OpenApiExample(
    response_only=True,
    name="추천영화 목록 조회",
    value=[
        {
            "id": 2,
            "user": 1,
            "genre": ["SF", "액션", "코메디"],
            "nation_korean": True,
            "nation_foreign": False,
            "period_2000": True,
            "period_2010": False,
            "period_2020": True,
            "movie_id": 5,
            "movie_title": "과속스캔들",
            "poster_url": "http://file.koreafilm.or.kr/thm/02/00/03/80/tn_DPK09869A.jpg",
            "movie": 5,
            "created_at": "2023-12-21T16:11:28.448801+09:00",
        },
        {
            "id": 1,
            "user": 1,
            "genre": ["가족", "드라마", "판타지"],
            "nation_korean": True,
            "nation_foreign": True,
            "period_2000": False,
            "period_2010": True,
            "period_2020": True,
            "movie_id": 4,
            "movie_title": "알라딘",
            "poster_url": "http://file.koreafilm.or.kr/thm/02/00/05/16/tn_DPF018168.jpg",
            "movie": 4,
            "created_at": "2023-12-21T16:09:51.471721+09:00",
        },
    ],
)
