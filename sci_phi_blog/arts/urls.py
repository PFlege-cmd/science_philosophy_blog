from .views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    show_categories, show_languages, ArticleByLanguageView, ResponseView, ResponseUpdateView, ResponseDeleteView, \
    ResponseToResponseView, ShowResponsesToResponseView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'arts'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create_article'),
    path('all/', ArticleListView.as_view(), name = 'all'),
    path('all/categories', show_categories, name ='categories'),
    path('all/languages', show_languages, name='languages'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article'),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name='update_article'),
    path('article/<int:pk>/delete', ArticleDeleteView.as_view(), name='delete_article'),
    path('article/<int:pk>/response', ResponseView.as_view(), name='comment_article'),
    path('article/<int:pk>/response/<int:pk_2>', ResponseUpdateView.as_view(), name='update_comment'),
    path('article/<int:pk>/response/<int:pk_2>/delete', ResponseDeleteView.as_view(), name='delete_comment'),
    path('article/response_to_response/<int:pk>', ResponseToResponseView.as_view(), name='response_to_response'),
    path('article/response_to_response/<int:pk>/all_responses', ShowResponsesToResponseView.as_view(), name='all_responses_to_response'),
    path('languages/<str:lang>', ArticleByLanguageView.as_view(), name='articles_by_lang'),
]