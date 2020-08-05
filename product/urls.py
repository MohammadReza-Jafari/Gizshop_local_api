from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetAllProductView.as_view(), name='product_list'),
    path('<int:pk>/', views.GetProductView.as_view(), name='single_product'),
    # admin url
    path('create/', views.CreateProductView.as_view(), name='create'),
    path('edit/<int:pk>/', views.EditProductView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('add-image/<int:product_id>/', views.AddImageToProductView.as_view(), name='add_image'),
    path('delete-image/<int:img_id>/', views.DeleteProductImageView.as_view(), name='delete_image'),
    path('get-price/<int:pk>/', views.GetProductPriceView.as_view(), name='get_price'),
    path('add-to-amazing/<int:pk>/', views.AddToAmazingOffer.as_view(), name='add_to_amazing'),
    path(
        'delete-from-amazing/<int:pk>/',
        views.DeleteFromAmazingOffers.as_view(),
        name='delete_from_amazing'
    ),
]
