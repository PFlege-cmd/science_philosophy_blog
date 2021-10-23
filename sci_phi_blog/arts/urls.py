from .views import ArticleCreateView, ArticleListView
from django.urls import path

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('all/', ArticleListView.as_view(), name = 'all'),
]