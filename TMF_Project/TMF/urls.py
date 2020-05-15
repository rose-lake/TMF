from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>', views.article_detail, name='article_detail'),
    path('article/<int:pk>/comment/', views.add_comment_to_article, name='add_comment_to_article'),
]
