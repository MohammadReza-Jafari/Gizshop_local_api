from django.urls import path, include

from . import views


urlpatterns = [
    path('category/', include([
        path('all-data/', views.GetAllCategoriesView.as_view(), name='get_all_data'),
        path('', views.CategoryListView.as_view(), name='category_list'),
        path('create/', views.CreateCategoryView.as_view(), name='create_category'),
        path('<int:pk>/', views.MangeCategoryView.as_view(), name='manage_category'),

    ])),
    path('main-category/', include([
        path('', views.MainCategoryListView.as_view(), name='main_category_list'),
        path('create/', views.CreateMainCategoryView.as_view(), name='create_main_category'),
        path('<int:pk>/', views.ManageMainCategoryView.as_view(), name='manage_main_category'),
    ])),
    path('sub-category/', include([
        path('', views.SubCategoryListView.as_view(), name='sub_category_list'),
        path('create/', views.CreateSubCategoryView.as_view(), name='create_sub_category'),
        path('<int:pk>/', views.MangeSubCategoryView.as_view(), name='manage_sub_category'),
    ])),







]