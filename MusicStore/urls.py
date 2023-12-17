from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from djoser.views import TokenDestroyView, TokenCreateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from instruments.views import (
    InstrumentListCreateView,
    OrderListCreateView,
    InstrumentDetailView,
    OrderDetailView,
    RegistrationAPIView, UserRegistrationView,
)

schema_view = get_schema_view(
    openapi.Info(
        title='Music Store',
        default_version="v1",
        description='This is music store!',
        terms_of_service='https://www.musicstore.com/terms/',
        contact=openapi.Contact(email='contact.musicstore@gmail.com'),
        license=openapi.License(name='Licenses'),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', InstrumentListCreateView.as_view(), name='home'),
    path('instruments/', InstrumentListCreateView.as_view(), name='instruments-list-create'),
    path('instruments/<int:pk>/', InstrumentDetailView.as_view(), name='instruments-detail'),
    path('orders/', OrderListCreateView.as_view(), name='orders-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='orders-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('api/token/', TokenCreateView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/registration/', UserRegistrationView.as_view(), name='registration'),
    # ...
]
