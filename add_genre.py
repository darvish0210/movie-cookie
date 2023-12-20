import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from movieinfo.models import Genre

if __name__ == "__main__":
    genres = [
        "SF",
        "가족",
        "갱스터",
        "공포",
        "공포(호러)",
        "교육",
        "군사",
        "기업ㆍ기관ㆍ단체",
        "느와르",
        "동성애",
        "드라마",
        "로드무비",
        "멜로/로맨스",
        "멜로드라마",
        "모험",
        "무협",
        "문화",
        "뮤지컬",
        "뮤직",
        "미스터리",
        "반공/분단",
        "범죄",
        "사회",
        "사회물(경향)",
        "서부",
        "스릴러",
        "스포츠",
        "시대극/사극",
        "신파",
        "실험",
        "아동",
        "애니메이션",
        "액션",
        "어드벤처",
        "역사",
        "옴니버스",
        "인권",
        "인물",
        "자연ㆍ환경",
        "재난",
        "전기",
        "전쟁",
        "종교",
        "지역",
        "첩보",
        "청춘영화",
        "코메디",
        "판타지",
        "하이틴(고교)",
        "합작(번안물)",
        "해양액션",
        "활극",
    ]
    for genre in genres:
        target = Genre.objects.create(genre=genre)
        target.save()
print("장르추가완료")
