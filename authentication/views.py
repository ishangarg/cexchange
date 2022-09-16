from distutils.log import error
from rest_framework import viewsets,status
from authentication.models import User
from authentication.serializers import CreateUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from authentication.models import TwoStepAuthModel

# @csrf_exempt
class CreateUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class loginView():
#     return viewSet(otpView)


class SimpleApI(APIView):
    
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):

        jwt_token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        access_token = AccessToken(jwt_token)
        user = User.objects.get(id=access_token['user_id'])

        content = {'email': user.email, 'password': user.password, 'user_id': user.id, 'date_joined': user.date_joined}
        return Response(content)    
        

class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        TwoStepAuthModel.objects.all().delete()

        token = TwoStepAuthModel.objects.create(token=serializer.validated_data)
        token.save()

        login_message = {"message": "Login Successful, Please enter the OTP"}

        return Response(login_message, status=status.HTTP_200_OK)



class OTPView(APIView):
    def post(self,request):
        otp = 12345
        if(request.data["otp"] == otp):
            return Response(TwoStepAuthModel.objects.all().first().token,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)