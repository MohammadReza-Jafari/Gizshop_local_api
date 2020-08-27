from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListArticleView.as_view(), name='articles_list'),
    path('<int:pk>/', views.SingleArticleView.as_view(), name='single_article'),
    path('vote/<int:pk>/', views.VoteArticleView.as_view(), name='vote'),
    path('create/', views.CreateArticleView.as_view(), name='create_article'),
    path('manage/<int:pk>/', views.ManageArticleView.as_view(), name='manage_article'),
]
