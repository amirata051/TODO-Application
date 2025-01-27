from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from tasks.views import home_view

schema_view = get_schema_view(
    openapi.Info(
        title="TODO Application API",
        default_version="v1",
        description="API documentation for TODO Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", home_view, name="home"),  # Home page
    path("admin/", admin.site.urls),
    path("api/", include("tasks.urls")),  # App's endpoints
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Swagger UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # ReDoc UI
]
