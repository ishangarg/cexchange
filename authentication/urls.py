from django.urls import path, include
from authentication.views import CreateUserView, SimpleApI

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenBlacklistView

router = routers.DefaultRouter()
router.register(r'signup', CreateUserView)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login_test/' , SimpleApI.as_view()),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
