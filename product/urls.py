from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetAllProductView.as_view(), name='get_all_product'),
    path('<int:pk>/', views.GetProductView.as_view(), name='manage_product'),
    path('create/', views.CreateProductView.as_view(), name='create'),
    path('edit/<int:pk>/', views.EditProductView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('add-image/<int:product_id>/', views.AddImageToProductView.as_view(), name='add_image'),
    path('delete-image/<int:img_id>/', views.DeleteProductImageView.as_view(), name='delete_image')
]
