# CRUD 가능한 커뮤니티



## A. 프로젝트 구조

pjt04/은 startproject 명령어로 생성되는 project 디렉토리
movies/는 startapp 명령어로 생성되는 application 디렉토리





## B. Model

정의할 모델 클래스의 이름은 Movie 이며 다음과 같은 정보를 저장합니다

| 필드명      | 자료형         | 설명        |
| ----------- | -------------- | ----------- |
| title       | String(<= 100) | 제목        |
| overview    | Text           | 줄거리      |
| poster_path | String(<= 500) | 포스터 경로 |



```python
# movies/models.py

class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=500) 
```

- 해당되는 조건을 field로 설정하여 class Movie 를 정의하였다.
- `$ python manage.py makemigrations` 명령어를 사용해 새로운 마이그레이션을 만든다.
- `$ python manage.py migrate`로 마이그레이션을 DB에 동기화한다.





## C. Admin
위에서 정의한 모델 Movie 는 관리자 페이지에서 데이터의 생성 조회 수정 삭제 가능해야 합니다



**admin 페이지에서 제목만 보는 경우**

```python
# movies/models.py

class Movie(models.Model):
    ...
    def __str__(self):
        return self.title
```

- Movie 안에 title을 리턴하는 함수를 만들어줍니다.

```python
# movies/admin.py

from django.contrib import admin
from .models import Movie

admin.site.register(Movie)
```

- model 에서 생성한 class인 Movie를 import 합니다.('.model'을 사용하여 import할 수 있는 것은 패키지 안에서만)
- `admin.site.register(Movie)`로 사이트에 관리자로 등록해줍니다.



 **admin 페이지에서 각각의 속성들의 값을 출력하도록 설정하는 경우**

- Model 클래스에 str 추가 x

```python
# movies/admin.py
...
class Admin_movie(admin.ModelAdmin):
    list_display = ('title', 'overview', 'poster_path')

admin.site.register(Movie, Admin_movie)
```

- 새로운 class를 만들고 () 안에 `admin.ModelAdmin` 작성
- list에 원하는 값을 넣어주고, 방금 만든 class 를 같이 등록해준다
- `/주소/admin/` 입력시 admin site로 이동한다.
- `$python manage.py createsuperuser`로 admin id, pw 등록한다







## D. URL

| URL 패턴               | 설명                    |
| ---------------------- | ----------------------- |
| /movies/new/           | 새로운 영화 작성 Form   |
| /movies/create/        | 영화 데이터 저장        |
| /movies/               | 전체 영화 목록 조회     |
| /movies/< pk>/         | 단일 영화 상세 조회     |
| /movies/< pk >/edit/   | 단일 영화 수정 Form     |
| /movies/< pk >/update/ | 수정된 영화 데이터 저장 |
| /movies/< pk >/delete/ | 단일 영화 삭제          |





```python
# pjt04/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls'))
]
```

- 각 app에 urls.py를 작성하여 프로젝트의 urls.py에서 각 앱의 urls.py로 url 매핑을 위탁한다. (`include('movies.urls')`)

- pjt04의 urls파일에 movies/경로를 포함시키고, include도 import해준다.



```python
# movies/urls.py
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit', views.edit, name='edit'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
]
```

- movies 폴더에 urls.py를 생성하고 같은 위치의 view함수를 import한다. 

- 이름 공간을 지정하여 url을 불러올 때 이름이 지정된 url을 고유하게 사용할 수 있다.(url은 : 를 사용하여 지정한다.)

- `<int:pk>`는 각 영화의 번호이므로, int 로 받아 view함수의 인자로 넘겨줄 수 있다. 





## E. View & Template

### i . 공유 탬플릿 생성 및 사용

```html
<a class="navbar-brand" href="{% url 'movies:index'%}">전체 영화 목록 조회</a>
```

- templates 폴더를 pjt04와 동일 선상에 생성한 후, base.html을 생성한다.

- bootstrap CDN을 head와 body에 각각 삽입하고, navbar template을 가져와서 삽입한다. navbar 아래에는 `{% block content %}` `{% end block%}`로 다른 html tag가 삽입될 공간을 마련한다.

- 다른 링크로 이동해야하므로 a tag를 사용하여 url을 삽입해준다. 

```python
# community/settings.py

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR/'templates'], 
        ...
    },
]
```

- base directory를 'templates'로 설정해준다.



### ii. 전체 영화 목록 조회

```python
# movies/views.py

...
from django.shortcuts import render
from .models import Movie

def index(request):
    movies = Movie.objects.order_by('-id')
    context = {
        'movies': movies
    }
    return render(request, 'movies/index.html', context)
...
```

- urls에서 name으로 `'index'` 를 받으면( `path('', views.index, name='index'),` ), movies/views.py에서 `def index(request)`가 실행된다. 

- `def index(request)`는 Movie 클래스를 통해 id의 내림차순으로 영화 목록을 받아와 movies에 저장하고 movies의 index.html을 리턴한다.



```python
# movies/templates/index.html

{% extends 'base.html' %}

{% block content %}
<h1>전체 영화 목록 조회</h1>
{% for movie in movies %}
  <a href="{% url 'movies:detail' movie.pk %}">{{ movie.title }}</a><br>
{% endfor %}
{% endblock content %}
```

- index.html은 base.html의 template을 상속받는다. `extends`와 `block`을 사용한다.

- for문을 사용하여 저장된 영화 목록인 movies의 제목을 출력하고, a tag를 통해 상세 페이지로 이동할 수 있다.

- url은 '지정한 이름공간(movies):파일명' 으로 지정 가능하다. 하지만 detail 함수는 pk가 요구되므로,  `movie.pk`를 같이 작성한다.





### iii. 새로운 영화 작성 Form

| 필드명      | HTML요소 | Type |
| ----------- | -------- | ---- |
| title       | input    | text |
| overview    | textarea | 없음 |
| poster_path | input    | text |



```html
# movies/new.html
<form action="{% url 'movies:create' %}" method='POST'>
  {% csrf_token %}
  <label for="title">title</label>
  <input type="text" id='title' name='title'><br>
 ...
  <input type="submit">
</form>
```

- form tag의 **method**를 GET or POST로 지정하여 서버로부터 데이터를 가져온다. method로 POST를 쓰는 경우, 보안 토큰` {% csrf_token %}` 을 입력한다.

- form tag의 **action**에는 받은 데이터를 보낼 url을 작성한다.

- **input** tag에는 name을 추가로 작성하여, create함수가 실행될 때 key의 value를 전달받을 수 있고, id값을 부여하여 label tag와 연결할 수 있다.

- **label** tag에는 input tag의 id 값과 동일한 값을 부여하여 제어할 수 있다.





### iv. 영화 데이터 저장

```python
# movies/views.py
def create(request):
    title = request.POST.get('title')
    ...
    movie  = Movie(title = title, overview=overview, poster_path=poster_path)
    movie.save()
    return redirect('movies:index')
```

- new.html에서 데이터를 전달받아, `{% url 'movies:create' %}` 로 보내면,  movies/url.py의 `path('create/', views.create, name='create'),` 로 인해 movies/view.py의 `def create(request)` 함수가 실행된다.

- request.POST에 저장된 데이터를 해당 key(name)으로 불러와 변수에 할당한다.

- class Movie의 값으로 방금 할당한 변수들을 movie에 할당하고, movie를 save한다.

- 저장이 완료되면 전체 영화 목록 조회 페이지(index.html)로 redirect한다.





### v. 단일 영화 상세 조회

```python
# movies/views.html

def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)
```

- 단일 영화를 조회하기 위해서는 영화의 primary key가 필요하다. Movie class의 pk를 받아와서 movie에 할당한 후, 'movie' key로 movie를 받아와야한다. 



```html
# movies/detail.html
...
<h1>{{ movie.title }}</h1>
<p>{{ movie.overview }}</p>
<p>{{ movie.poster_path}}</p>

<a href="{% url 'movies:edit' movie.pk %}">수정</a><br>
<a href="{% url 'movies:delete' movie.pk %}">삭제</a>
...
```

- 변수명 movie에 '.'을 통해 변수 속성에 접근할 수 있다.

- 단일 정보를 수정하고 삭제하는 기능을 추가하였다.





#### [추가 기능 상세 - 수정]

```python
# movies/views.py

def edit(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/edit.html', context)
```

- `<a href="{% url 'movies:edit' movie.pk %}">수정</a><br>` 을 클릭하면, url에서 views.py의 edit 함수가 실행된다. 특정 영화를 수정하는 것이므로 pk를 같이 받는다.



```html
# movies/edit.html
...
<form action="{% url 'movies:update' movie.pk %}" method='POST'>
  {% csrf_token %}
  <label for="title">title</label>
  <input type="text" id='title' name='title' value='{{ movie.title }}'><br>
  <label for="overview">overview</label>
  <textarea name="overview" id="overview" cols="30" rows="10">{{ movie.overview }}</textarea><br>
  ...
</form>
```

- edit 함수는 이미 있는 내용을 수정하는 것이므로, 이전에 입력한 내용을 불러와서 기존 input/ textarea에 넣어주어야 한다.

- input tag의 경우 `value` 로 변수를 추가해준다.

- textarea의 경우 여는 태그와 닫는 태그 사이에 변수를 추가한다.

- 내용을 수정하고 제출하면 `update` url이 실행된다.



```python
# movies/view.py

def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.title = request.POST.get('title')
    ...
    movie.save()
    return redirect('movies:index')
```

- 새로 입력받은 데이터를 기존 데이터에 재할당한다.
- 저장 후 기존 페이지로 되돌아간다.



#### [추가 기능 상세 - 삭제]

```python
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete()

    return redirect('movies:index')
```

- `<a href="{% url 'movies:delete' movie.pk %}">삭제</a>` 를 누르면 urls.py의 delete 경로를 통해 delete 함수가 불러와진다.
- 전달 받은 pk 값을 이용해 삭제하고자 하는 movie를 변수movie에 저장하고, movie를 삭제한다.
- 삭제 후 전체 영화 목록으로 redirect 해준다.



