from django.urls import path, include

from . import views

app_name = 'product'
urlpatterns = [
    path('product/', include([
        path('', views.GetAllProductView.as_view(), name='product_list'),
        path('<int:pk>/', views.GetProductView.as_view(), name='details'),
        # admin url
        path('create/', views.CreateProductView.as_view(), name='create'),
        path('edit/<int:pk>/', views.EditProductView.as_view(), name='edit'),
        path('delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete'),
        path('get-price/<int:pk>/', views.GetProductPriceView.as_view(), name='get_price'),
        path('add-to-amazing/<int:pk>/', views.AddToAmazingOffer.as_view(), name='add_to_amazing'),
        path(
            'delete-from-amazing/<int:pk>/',
            views.DeleteFromAmazingOffers.as_view(),
            name='delete_from_amazing'
        ),
    ])),
    path('image/', include([
        path('add/<int:product_id>/', views.AddImageToProductView.as_view(), name='add_image'),
        path('delete/<int:img_id>/', views.DeleteProductImageView.as_view(), name='delete_image'),
    ])),
    path('search/', include([
        path(
            'main-category/<int:main_category_id>/',
            views.GetProductByMainCategory.as_view(),
            name='search_by_main_category'
        ),
        path(
            'category/<int:category_id>/',
            views.GetProductByCategory.as_view(),
            name='search_by_category'
        ),
        path(
            'sub-category/<int:sub_category_id>/',
            views.GetProductBySubCategory.as_view(),
            name='search_by_sub_category'
        )
    ]))

]
