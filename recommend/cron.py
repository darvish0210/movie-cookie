# recommend/cron.py
import os
import sys
import django

sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import csv
import logging
import re
import requests
import pandas as pd
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from movieinfo.models import Genre


class RequestFailedError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def process_movies(country_code, csv_file_name):
    # kobis API 정보
    kobis_api_key = str(settings.KOBIS_API_KEY)
    kobis_base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

    # 어제 날짜 구하기
    yesterday = timezone.now() - timedelta(1)
    target_date = yesterday.strftime("%Y%m%d")

    # kobis API 요청 보내기
    params = {
        "key": kobis_api_key,
        "targetDt": target_date,
        "repNationCd": country_code,
    }
    response = requests.get(kobis_base_url, params=params)

    try:
        data = response.json()
        movie_data = data["boxOfficeResult"]["dailyBoxOfficeList"]
    except Exception as e:
        logging.error(f"{country_code}: KOBIS API 요청에 실패했습니다: {e}")
        raise RequestFailedError("KOBIS API 요청에 실패했습니다.") from None

    # kmdb API 정보
    kmdb_api_key = str(settings.KMDB_API_KEY)
    kmdb_base_url = (
        "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp"
    )

    # CSV 파일 열기
    try:
        with open(csv_file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            movies = list(reader)
    except FileNotFoundError:
        logging.error(f"파일을 찾을 수 없습니다: {csv_file_name}")
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {csv_file_name}") from None

    # kmdb API 요청 보내고 CSV 파일 업데이트: movie_data는 KOBIS 결과값
    for movie in movie_data:
        movie_name = movie["movieNm"]
        movie_open_date = movie["openDt"]
        movie_audience = movie["audiAcc"]

        # kmdb API 호출
        kmdb_params = {
            "collection": "kmdb_new2",
            "ServiceKey": kmdb_api_key,
            "title": movie_name,
            "listCount": 1,
            "detail": "N",
            "movieId": country_code,
            "releaseDts": movie_open_date[:4] + "0101",
            "releaseDte": movie_open_date[:4] + "1231",
        }
        kmdb_response = requests.get(kmdb_base_url, params=kmdb_params)

        if kmdb_response.status_code == 200:
            kmdb_data = kmdb_response.json()

            if kmdb_data["TotalCount"] == 0:
                print(f'극영화에서 "{movie_name}"에 대한 kmdb 데이터를 찾을 수 없습니다. 비극영화로 다시 검색합니다.')

                # 다시 검색을 위해 movieId 변경 후 재검색
                if country_code == "K":
                    kmdb_params["movieId"] = "A"
                elif country_code == "F":
                    kmdb_params["movieId"] = "B"

                # 다시 요청
                kmdb_response = requests.get(kmdb_base_url, params=kmdb_params)
                if kmdb_response.status_code == 200:
                    kmdb_data = kmdb_response.json()
                else:
                    logging.error(f'"{movie_name}"에 대한 kmdb 데이터를 찾을 수 없습니다.')
                    continue

            if kmdb_data["TotalCount"] != 0:
                kmdb_movie = kmdb_data["Data"][0]["Result"][0]

                kmdb_title = kmdb_movie["title"]
                kmdb_title = re.sub(r" \!HS ", "", kmdb_title)
                kmdb_title = re.sub(r" \!HE ", "", kmdb_title)
                kmdb_title = re.sub(r"^\s+|\s+$", "", kmdb_title)
                kmdb_title = re.sub(r" +", " ", kmdb_title)

                kmdb_genre_list = kmdb_movie["genre"]
                kmdb_genre_list = re.sub(", *", "|", kmdb_genre_list)

                kmdb_doc_id = kmdb_movie["DOCID"]
                movie_id = kmdb_doc_id[0]
                movie_seq = kmdb_doc_id[1:]

                # CSV 파일 업데이트
                existing_movie = next(
                    (m for m in movies if m["kmdb제목"] == kmdb_title), None
                )
                if existing_movie:
                    existing_movie["관객수"] = movie_audience
                else:
                    new_movie = {
                        "번호": country_code + str(len(movies) + 1),
                        "kmdb제목": kmdb_title,
                        "kmdb장르": kmdb_genre_list,
                        "개봉연도": movie_open_date[:4],
                        "관객수": movie_audience,
                        "movie_id": movie_id,
                        "movie_seq": movie_seq,
                    }
                    movies.append(new_movie)
            else:
                logging.error(f'"{movie_name}"에 대한 kmdb 데이터를 찾을 수 없습니다.')
                continue
        else:
            logging.error("KMDB API 요청에 실패했습니다.")
            raise RequestFailedError("KMDB API 요청에 실패했습니다.") from None

    # CSV 파일 업데이트 이전에 관객수에 따라 영화 정렬하기
    movies.sort(key=lambda x: int(x["관객수"]), reverse=True)

    # CSV 파일 저장
    fieldnames = ["번호", "kmdb제목", "kmdb장르", "개봉연도", "관객수", "movie_id", "movie_seq"]
    with open(csv_file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies)
    return "complete"


def genre_list(korean, foreign):
    # 두 개의 CSV 파일 경로
    korean_file_path = korean
    foreign_file_path = foreign

    # 두 개의 CSV 파일을 각각 DataFrame으로 읽기
    korean_data = pd.read_csv(korean_file_path)
    foreign_data = pd.read_csv(foreign_file_path)

    # 각각의 파일에서 장르 컬럼 선택 후 모든 장르를 |로 분할하여 리스트에 추가
    all_genres = []
    for genres in korean_data["kmdb장르"]:
        genres_split = genres.split("|")
        all_genres.extend(genres_split)

    for genres in foreign_data["kmdb장르"]:
        genres_split = genres.split("|")
        all_genres.extend(genres_split)

    # 중복 제거를 위해 set으로 변환 후 다시 리스트로 변환하고 가나다 순으로 정렬
    unique_genres = sorted(list(set(all_genres)))

    return unique_genres


def update_csv():
    try:
        korean = process_movies("K", settings.BASE_DIR / "static/korean.csv")
    except RequestFailedError:
        korean = process_movies("K", settings.BASE_DIR / "static/korean.csv")
    try:
        foreign = process_movies("F", settings.BASE_DIR / "static/foreign.csv")
    except RequestFailedError:
        foreign = process_movies("F", settings.BASE_DIR / "static/foreign.csv")

    if korean == "complete":
        print("국내영화 업데이트 완료")
    if foreign == "complete":
        print("해외영화 업데이트 완료")

    genres = genre_list(
        settings.BASE_DIR / "static/korean.csv",
        settings.BASE_DIR / "static/foreign.csv",
    )

    for genre in genres:
        target, created = Genre.objects.get_or_create(genre=genre)
        if created:
            target.save()
    print("장르추가완료")
