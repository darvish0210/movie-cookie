# 231229 - 프로젝트 feedback

## 개인적인 피드백

- 1. post에 ```viewcount``` 속성을 넣어놨었다. 조회수를 카운팅 하려는 목적이었는데, 시간 부족상 포기하고 쓰지 못했다. 마찬가지로 수정시간 속성도 쓰지 못했다.
- 2. 기능구현에 우선한 나머지, 중복된 기능을 함수화하지 않았거나 컨벤션을 지키지 못한 부분도 많을거라 생각한다.
     컨벤션은 vscode의 blackFormatter 익스텐션이 어느정도 도와줬을거 같지만, css나 js 부분에서의 id, class 네이밍에서 허겁지겁 했던 것이 걸린다.
- 3. css에는 신경을 덜 써서 디자인적으로 부족한 점이 있었다. 대댓글 달기창이나 수정하기 창에는 버튼이 기본 html 버튼이 들어갔던 것 등 



## 심사받고 받았던 피드백 

---
### 1. 댓글 삭제시, 하위댓글 삭제
```
댓글1
ㄴ대댓글2
ㄴ대대댓글1
ㄴ대댓글3
댓글2
댓글3
...

```

인 구조일 때, ```댓글1``` 을 삭제하면 댓글1에 딸린 ```대댓글2```,```대대댓글1```,```대댓글3```도 같이 삭제되어 없어지는 이슈

---

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self", related_name="reply", on_delete=models.CASCADE, blank=True, null=True
    )
```

이는 내가 ```parent``` 속성에 ```on_delete=models.CASCADE``` 를 넣었기에 생긴것이라 생각한다.

사실 처음엔 당연히 같이 없어지는게 맞다고 생각했다. 게시글이 삭제될 때 댓글도 같이 사라지듯이, 대댓글이란 일종의 댓글1 과 대댓글2 끼리의 대화? 같다는 느낌으로 댓글1이 없으면 대댓글2의 의미가 딱히 없어지는게 아닐까 싶기도 했다.

근데 다시 생각해보니, 실 사용 커뮤니티 서비스 등에서는 '삭제되었습니다' 등이 남아서 삭제된 흔적은 알려주는 경우가 많았다.

---

개선하려면?

- ```on_delete=models.CASCADE``` 속성 제거하고, 댓글 delete 함수 재설계하기 : 없어진 빈 자리를 어떻게 표시할 지에 대한 render함수의 재설계가 필요.

---
### 2. 무한 depth 이슈

 내가 구상한 ```comment``` DB 구조
 
```
Table comment {
  
  id integer [primary key]
  content text
  user_id integer
  parent_id integer [default:null]
  post_id integer
  created_at date
  updated_at date


}
Ref: "comment"."parent_id" < "comment"."id"
```

```comment.id```를 그대로 받기에, 무한히 자기 자식을 만들어 나갈 수 있는 구조이다.
이 '무한'을 허용한 커뮤니티도 있긴 했지만, 네이버, 카카오등 큰 규모의 사이트는 이런 구조를 하지 않고 있었다. 피드백에서는 db에 무리가 간다고 했었다.

---

개선하려면? 

- 구조를 바꾸어 무한을 허용하지 않기: ```recomment``` 객체를 따로 만들어서 대댓글 1회 정도만 허용하기 등의 방안이 있을거라 생각한다.
- 횟수를 제한하여 무한을 허용하지 않기: count를 따로 두어, 일정 카운트 이상은 대댓글 달기 금지하기?


