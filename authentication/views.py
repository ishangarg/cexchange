from django.contrib.auth import get_user_model, authenticate, login
import json
# from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import re


# @csrf_exempt  #added for api testing via postman
def CreateUserView(request):
    User = get_user_model()  

    request_body_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_body_unicode)

    #TODO: Email and password verification needed. 

    response_data = dict()

    try:
        user = User.objects.create_user(email=request_body['email'],
                                 password=request_body['password'])
        user.save()
        
        response_data["code"] = 200
        response_data["message"] = "Sign up successful"
    except:
        response_data["code"] = 500
        response_data["message"] = "Sign up Failed, User exists"

    #TODO: user_creation validation needs to be done, to send appropriate response

    # Hard coded response.
 
    return JsonResponse(response_data)



# @csrf_exempt
def AuthenticateUserView(request):

    request_body_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_body_unicode)

    email = request_body['email']
    password = request_body['password']

    user = authenticate(username=email, password=password)

    response_data = dict()

    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
        # print("success")
        response_data["code"] = 200
        response_data["message"] = "Login successful"
    else:
        response_data["code"] = 403
        response_data["message"] = "Login Failed"

    return JsonResponse(response_data)
