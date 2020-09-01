from django.urls import path, include

from . import views

app_name = 'cart'
urlpatterns = [
    path('cart/', include([
        path('', views.GetAllCaretView.as_view(), name='list'),
        path('<int:pk>/', views.GetSingleCaretView.as_view(), name='details'),
        path('add/<int:product_id>/', views.AddToCaretView.as_view(), name='add_product')
    ]))
]
