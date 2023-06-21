from django.urls import path
from .views import (
   NewsList, NewDetail, NewsCreate, NewsUpdate, PostDelete, SearchList,
   CategoriesList, CategoryDetail, subscribe, unsubscribe, Index
)

# from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page

urlpatterns = [

   # path('', NewsList.as_view(), name='post_list'),
   path('', cache_page(60)(NewsList.as_view()), name='post_list'),

   # path('<int:pk>', NewDetail.as_view(), name='post_detail'),
   path('<int:pk>', cache_page(60*5)(NewDetail.as_view()), name='post_detail'),

   path('search/', SearchList.as_view(), name='post_search'),

   path('create/', NewsCreate.as_view(), name='create_news'),

   path('<int:pk>/update/', NewsUpdate.as_view(), name='update_news'),

   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('categories/', CategoriesList.as_view(), name='categories'),
   path('categories/<int:pk>/', CategoryDetail.as_view(), name='one_category'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

   path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),

   path('news/index/', Index.as_view()),

]