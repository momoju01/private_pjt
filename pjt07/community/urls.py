from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [

    path('create/', views.create_review, name='create'),
    path('', views.review_index, name='index'),
    path('<int:review_pk>/', views.review_detail, name='detail'),
    path('<int:review_pk>/update/', views.update_review, name='update'),
    path('<int:review_pk>/delete/', views.delete_review, name='delete'),
    path('<int:review_pk>/like/', views.like_review, name='like'),
    path('<int:review_pk>/comments/create/', views.create_comment, name='comment'),
]
