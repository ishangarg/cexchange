from django.urls import path, include

from authentication.views import CreateUserViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'auth', CreateUserViewSet)


urlpatterns = [
    # path('create/', CreateUserView),
    # path('login/', AuthenticateUserView),
    path('', include(router.urls)),
]


# signup/
# login/