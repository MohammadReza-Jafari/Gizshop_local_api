from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='url helpers')


admin.autodiscover()

urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('user/', include('user.urls')),
    path('category/', include('category.urls')),
    path('product/', include('product.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
