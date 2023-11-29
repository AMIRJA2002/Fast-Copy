from .services import RegisterUser, LoginUser, generate_login_otp, ValidateLogin
from .data_transfer.repository import UserRepository, LoginOTPRepository
from .data_transfer.filter_builder import UserFilterBuilder
from .custom_jwt_token import get_tokens_for_user
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status

User = get_user_model()


class RegisterUserAPI(APIView):

    class InputSerializer(serializers.Serializer):
        phone_number = serializers.CharField(max_length=11)
        password = serializers.CharField(max_length=50)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'last_login', 'phone_number', )

    def get(self, request, *args, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        user = RegisterUser(repository=UserRepository).create_user(data=data.data)
        return Response(self.OutputSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginUserAPI(APIView):

    class InputSerializer(serializers.Serializer):
        phone_number = serializers.CharField(max_length=11)

    def post(self, request, *args, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user_filter_builder = UserFilterBuilder(
            phone_number=data.data.get('phone_number'),
            is_active=True
        )

        otp = generate_login_otp()
        login_user = LoginUser(repository=UserRepository, dict_filter=user_filter_builder.get_dict_filter())
        login_user.check_phone_number()
        login_user.store_otp_in_cache(repository=LoginOTPRepository, otp=otp)

        return Response({'message': 'a six digit code sent to you'}, status=status.HTTP_200_OK)


class CheckOPTAndReturnJWTTokenAPI(APIView):
    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField(max_length=6)

    def post(self, request, *args, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        phone_number = request.data.get('phone_number', None)
        otp = data.data.get('otp', None)

        validate_login = ValidateLogin(repository=LoginOTPRepository, phone_number=phone_number, otp=otp)
        validate_login.check_otp()
        validate_login.delete_used_keys()

        dict_filter = UserFilterBuilder(phone_number=phone_number)
        user = ValidateLogin.get_user_object(repository=UserRepository, dict_filter=dict_filter.get_dict_filter())

        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)


class FastToken(APIView):
    """
    this is class for development and mosttttttt delete for production
    """
    def get(self, request):
        phone = request.data.get('phone')
        user = User.objects.get(phone_number=phone)
        response = get_tokens_for_user(user)
        return Response(response)
