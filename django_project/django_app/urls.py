from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, OrderViewSet
from .views import ProductListView, ProductDetailView, ProductCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Software engineering lab",
        default_version="v1",
        description="API documentation for the lab",
        ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
)




router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/products/', ProductListView.as_view(),
    name='product_list'),
    path('user/products/<int:pk>/', ProductDetailView.as_view(),
    name='product_detail'),
    path('user/products/new/', ProductCreateView.as_view(),
    name='product_create'),
    path('api/token/', TokenObtainPairView.as_view(),
    name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
    name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger',
    cache_timeout=0), name='schema-swagger-ui'),
]