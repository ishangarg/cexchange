from django.urls import path

from authentication.views import CreateUserView, AuthenticateUserView
# url

urlpatterns = [
    path('create/', CreateUserView),
    path('login/', AuthenticateUserView)
]


# signup/
# login/