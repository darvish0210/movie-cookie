from drf_spectacular.utils import OpenApiExample

GENERATE_REQUEST = OpenApiExample(
    request_only=True,
    name="영화 추천 받기",
    value={
        "input_nation": "국내|해외",
        "input_period": "2010년대|2020년대",
        "input_genre": "코메디|드라마|액션",
    },
)

GENERATE_RESPONSE = OpenApiExample(
    response_only=True,
    name="추천된 영화",
    value={
        "input_nation": "국내|해외",
        "input_period": "2010년대|2020년대",
        "input_genre": "코메디|드라마|액션",
        "movie_id": 10,
        "movie": {
            "id": 10,
            "searchTitle": "국제시장",
            "title": "국제시장",
            "posters": "http://file.koreafilm.or.kr/thm/02/00/03/25/tn_DPK010401.JPG|http://file.koreafilm.or.kr/thm/02/00/03/26/tn_DPK010414.JPG|http://file.koreafilm.or.kr/thm/02/00/03/23/tn_DPK010346.jpg|http://file.koreafilm.or.kr/thm/02/00/03/23/tn_DPK010347.jpg",
            "vods": '{"vodClass": "국제시장 [티저]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035114_P02.mp4"}|{"vodClass": "국제시장 [둘러보기 영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035149_P02.mp4"}|{"vodClass": "국제시장 [꽃분이네 가족영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035293_P02.mp4"}|{"vodClass": "국제시장 [30초]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035322_P02.mp4"}|{"vodClass": "국제시장 [설민석 현대사강의 영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035324_P02.mp4"}|{"vodClass": "국제시장 [메인]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035397_P02.mp4"}|{"vodClass": "국제시장 [국제시장 늬우스 영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035398_P02.mp4"}|{"vodClass": "국제시장 [제작기영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035445_P02.mp4"}|{"vodClass": "국제시장 [남진 인사영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035447_P02.mp4"}|{"vodClass": "국제시장 [설민석 스페셜강의]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035495_P02.mp4"}|{"vodClass": "국제시장 [새해인사영상]", "vodUrl": "https://www.kmdb.or.kr/trailer/trailerPlayPop?pFileNm=MK035588_P02.mp4"}',
            "directors": "윤제균",
            "actors": "황정민|김윤진|오달수|정진영|장영남|라미란|김슬기|이현|김민재|태인호|황선화|엄지성|장대웅|신린아|이예은|최재섭|정영기|유정호|맹세창|홍석연|CHOE STELLA KIM|고윤|남진복|박선웅|황인준|정윤호|박영수|조연호|박예은|신지아|김재현|김설|박용제|박재완|박재우|진선미|박시아|손미소|손누리|김재철|길호성|성낙경|Michala B??zov?|James Kneafsey|Ryan James|Matthew Ryan Douma|염시훈|김춘기|NGUYEN MAI CHI|Richard Liewellyn Wilson|Conor Doyle|차승호|김진혁|정재민|박정승|최원|Jesse Day|이동욱|정기섭|Norbert ?id|Petr V?gner|신도훈|한철우|Ji?? Vojta|Petr Hlavi?ka|Daniel Sommer|Miroslav Navr?til|David Bene?|Jakub Vindi?|Norbert ?id|Petr V?gner|Teresa Trnkov?|염상태|안정우|유재상|김선영|김수웅|손영순|최유찬|오승환|김나희|정찬우|박상혁|전성훈|전희경|이종석|윤영경|Anfuman|Syarat|박성민|류경현|김리하|Lstavan Medvigy|장영주|박혜진|현봉식|Andrew William Brand|이준철|박진수|강신철|Wattana Kumklong|Nascha Charerndee|Wasin Koednana|Pumpat Rodpai|Andrea Pini|유성곤|엄준필|황창기|이연기|김동준|이진희|손동일|손동철|허종오|박인옥|김예빈|김우진|이민영|이소영|김지영|원인식|이희성|신정섭|강신구|김기주|하철|김남륜|김병찬|정용규|김현중|이원섭|황진호|조미초|김동원|김현창|허동원|박경애|김운자|강희중|서윤하|박재영|임태진|백낙순|김현숙|김정|김하연|박찬미|이도군 박재언|장우영|박길수|Ennik Somi Douma|김은해|이순환|강영하|한율|남규백|박진서|오은수|남승우|김윤용|이건희|이민우|이재순|Evelyn Maverick Douma|서울예술대학교 연기과 학생 일동|박찬희|정성호|황인준|박혜진|김설|유재상|김근영",
            "nations": "대한민국",
            "companies": "㈜JK필름|씨제이엔터테인먼트㈜",
            "plot": "가장 평범한 아버지의 가장 위대한 이야기’1950년대 한국전쟁 이후로부터 현재에 이르기까지 격변의 시대를 관통하며 살아온 우리 시대 아버지 ‘덕수’(황정민 분), 그는 하고 싶은 것도 되고 싶은 것도 많았지만 평생 단 한번도 자신을 위해 살아본 적이 없다. ‘괜찮다’ 웃어 보이고 ‘다행이다’ 눈물 훔치며 힘들었던 그때 그 시절, 오직 가족을 위해 굳세게 살아온 우리들의 아버지 이야기가 지금부터 시작된다.",
            "runtime": 126,
            "rating": "12세관람가",
            "genres": "드라마",
            "releaseDate": "2014-12-17",
        },
    },
)

RECOMMEND_REQUEST = OpenApiExample(
    request_only=True,
    name="영화 추천 저장/수정",
    value={
        "input_nation": "국내|해외",
        "input_period": "2010년대|2020년대",
        "input_genre": "코메디|드라마|액션",
        "movie_id": 10,
    },
)

RECOMMEND_RESPONSE = OpenApiExample(
    response_only=True,
    name="저장/수정된 추천영화",
    value={
        "user": 1,
        "input_genre": "코메디|드라마|액션",
        "input_nation": "국내|해외",
        "input_period": "2010년대|2020년대",
        "movie_id": 10,
        "movie": 10,
    },
)

RECOMMEND_LIST = OpenApiExample(
    response_only=True,
    name="추천영화 목록 조회",
    value=[
        {
            "user": 1,
            "input_genre": "드라마|판타지",
            "input_nation": "해외",
            "input_period": "2000년대|2020년대",
            "movie_id": 13,
            "movie": 13,
        },
        {
            "user": 1,
            "input_genre": "코메디|드라마|액션",
            "input_nation": "국내|해외",
            "input_period": "2010년대|2020년대",
            "movie_id": 10,
            "movie": 10,
        },
    ],
)
