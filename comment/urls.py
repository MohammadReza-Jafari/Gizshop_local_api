from django.urls import path

from . import views


urlpatterns = [
    path('<int:product_id>/', views.ProductCommentListView.as_view(), name='product_comments'),
    path('add/<int:product_id>/', views.AddCommentView.as_view(), name='add_comment'),
    # admin url
    path('not-accepted/', views.NotAcceptedCommentListView.as_view(), name='not_accepted_comments'),
    path('accept/<int:pk>/', views.AcceptCommentView.as_view(), name='accept_comment'),
    path('delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete_comment'),
]
