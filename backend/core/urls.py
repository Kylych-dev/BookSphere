from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Books API",
      default_version='v1',
      description="API для работы с книгами и авторами",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@booksphere.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.router')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='swagger-schema'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
