import json
import re
from pathlib import Path

import environ
from openai import OpenAI

from .models import MovieInfo, OneLineCritic

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
env.read_env(BASE_DIR / ".env")

client = OpenAI()
OpenAI.api_key = env("OPENAI_API_KEY")


def create_GPT_report(data):
    question = json.dumps(data, ensure_ascii=False)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "너는 서비스 유저들에게 영화 추천 메시지를 생성하는 영화 큐레이터다.",
            },
            {
                "role": "system",
                "content": """
                user의 입력은 포멧은 다음과 같다: {'title': '영화 제목', 'plot': '영화 줄거리', 'genre': '영화 장르', 'critics': '영화 한줄평의 목록'}
                
                너는 다음과 규칙을 통해 영화를 추천하는 매우 짧은 메시지를 생성해야 한다.
                규칙1: 영화 추천 메시지는 'title'로 전달된 '영화 제목'에 대한 영화에 대해서만 작성한다. 
                규칙2: 'plot'로 전달된 '영화 줄거리' 값을 통해 '영화 제목'에 대한 개략적인 전개와 분위기를 요약하는 메시지를 한 문장으로 작성한다.
                규칙3: '영화 줄거리'와 함께 'genre'로 들어온 '영화 장르' 값으로, 이 영화의 장르 정보를 통해 어떤 사람들이 이 영화를 좋아할지 분석하는 내용을 추가해도 좋다.
                규칙4: 'critics'로 들어온 '영화 한줄평의 목록'은 문자열 사이에 '|'가 있다. 이는 각각의 다른 사람의 한줄평을 구분하기 위해 넣은 것이다. 만약, '영화 한줄평의 목록'이 빈 값이면, 규칙5를 수행하지 않는다.
                규칙5: '영화 한줄평의 목록'을 분석하여 최근 이 영화에 대해 사람들이 어떤 생각을 가지는지 짧게 요약해서 메시지를 작성한다.
                규칙6: 규칙1, 규칙2, 규칙3, 규칙4, 규칙5의 모든 조건을 사용하여 영화를 추천하는 이하의 메시지를 생성한다.
                규칙7: 규칙 6으로 생성된 메시지의 길이는 50자를 넘지 않아야한다.
                """,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message.content
    # print(answer)
    return answer


def send_data_to_GPT(movie_id):
    movie = MovieInfo.objects.get(id=movie_id)
    critics = OneLineCritic.objects.filter(movie=movie).order_by("created_at")[:10]

    critic_msg = ""

    for ciritic in critics:
        critic_msg += f"{ciritic.content}|"
    critic_msg = critic_msg[:-1]

    data = {
        "title": movie.title,
        "plot": movie.plot,
        "genre": re.sub(r"\|", ", ", movie.genres),
        "critics": critic_msg,
    }
    # print(data)
    message = create_GPT_report(data)
    return message
