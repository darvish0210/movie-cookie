from drf_spectacular.utils import OpenApiExample

GENERATE_REQUEST = OpenApiExample(
    request_only=True,
    name="영화 추천 받기",
    value={
        "genre": ["드라마", "코메디", "멜로/로맨스"],
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
        "genre": ["드라마", "코메디", "멜로/로맨스"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
        "movie_id": 7,
        "movie_title": "국제시장",
        "poster_url": "http://file.koreafilm.or.kr/thm/02/00/03/25/tn_DPK010401.JPG",
    },
)

RECOMMEND_REQUEST = OpenApiExample(
    name="추천된 영화",
    request_only=True,
    value={
        "genre": ["드라마", "코메디", "멜로/로맨스"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
        "movie_id": 7,
        "movie_title": "국제시장",
        "poster_url": "http://file.koreafilm.or.kr/thm/02/00/03/25/tn_DPK010401.JPG",
    },
)

RECOMMEND_RESPONSE = OpenApiExample(
    response_only=True,
    name="저장/수정된 추천영화",
    value={
        "user": 1,
        "genre": ["드라마", "멜로/로맨스", "코메디"],
        "nation_korean": True,
        "nation_foreign": True,
        "period_2000": False,
        "period_2010": True,
        "period_2020": True,
        "movie_id": 7,
        "movie_title": "국제시장",
        "poster_url": "http://file.koreafilm.or.kr/thm/02/00/03/25/tn_DPK010401.JPG",
        "movie": 7,
    },
)

RECOMMEND_LIST = OpenApiExample(
    response_only=True,
    name="추천영화 목록 조회",
    value=[
        {
            "user": 1,
            "genre": ["SF", "스릴러", "액션"],
            "nation_korean": False,
            "nation_foreign": True,
            "period_2000": True,
            "period_2010": False,
            "period_2020": True,
            "movie_id": 9,
            "movie_title": "트랜스포머",
            "poster_url": "http://file.koreafilm.or.kr/thm/02/00/00/95/tn_DPF000123.jpg",
            "movie": 9,
        },
        {
            "user": 1,
            "genre": ["드라마", "멜로/로맨스", "코메디"],
            "nation_korean": True,
            "nation_foreign": True,
            "period_2000": False,
            "period_2010": True,
            "period_2020": True,
            "movie_id": 7,
            "movie_title": "국제시장",
            "poster_url": "http://file.koreafilm.or.kr/thm/02/00/03/25/tn_DPK010401.JPG",
            "movie": 7,
        },
    ],
)
