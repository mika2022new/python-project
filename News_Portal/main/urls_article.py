from django.urls import path
from .views import NewsList, ArticleCreate, ArticleUpdate, PostDelete

urlpatterns = [

   path('', NewsList.as_view(), name='post_list'),

 
   path('create/', ArticleCreate.as_view(), name='create_article'),

   path('<int:pk>/update/', ArticleUpdate.as_view(), name='update_article'),

   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]