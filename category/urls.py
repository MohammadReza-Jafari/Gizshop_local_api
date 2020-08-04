from django.urls import path

from . import views


urlpatterns = [
    path('get-all/', views.GetAllCategoriesView.as_view(), name='get_all_data'),
    path('create-main-category/', views.CreateMainCategoryView.as_view(), name='create_main_category'),
    path('main/', views.MainCategoryListView.as_view(), name='main_category_list'),
    path('main/<int:pk>/', views.ManageMainCategoryView.as_view(), name='manage_main_category'),
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/', views.MangeCategoryView.as_view(), name='manage_category'),
    path('create-sub-category/', views.CreateSubCategoryView.as_view(), name='create_sub_category'),
    path('sub/', views.SubCategoryListView.as_view(), name='sub_category_list'),
    path('sub/<int:pk>/', views.MangeSubCategoryView.as_view(), name='manage_sub_category'),
]