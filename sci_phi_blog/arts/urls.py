from .views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    show_categories, show_languages, ArticleByLanguageView
from django.urls import path

app_name = 'arts'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('all/', ArticleListView.as_view(), name = 'all'),
    path('all/categories', show_categories, name ='categories'),
    path('all/languages', show_languages, name='languages'),
    path('article/<int:pk>',ArticleDetailView.as_view(), name='article'),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name='update_article'),
    path('article/<int:pk>/delete', ArticleDeleteView.as_view(), name='delete_article'),
    path('languages/<slug:lang>', ArticleByLanguageView.as_view(), name='articles_by_lang'),
]