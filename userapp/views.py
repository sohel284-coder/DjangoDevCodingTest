from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from transactionapp.models import Balance

from userapp.serializers import *



# Register API
class UserRegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        ### new user will get 100 taka 
        Balance.objects.create(user=user, current_balance=100, previous_balance=0, )
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


#User Login Api
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)
        except:
            return Response('Given Credential is not valid', status=status.HTTP_401_UNAUTHORIZED)    