from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from events_api.models import Event


# МОЙ СЕРИАЛИЗАТОР ПОЛЬЗОВАТЕЛЯ
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')


# МОЙ СЕРИАЛИЗАТОР РЕГИСТРАЦИИ
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED,
                                   error_messages={"invalid": "некорректный email", 'blank': 'заполните поле email'})
    username = serializers.CharField(required=settings.ACCOUNT_USERNAME_REQUIRED, write_only=True,
                                     error_messages={"blank": "заполните поле username", })
    password1 = serializers.CharField(required=True, write_only=True,
                                      error_messages={'blank': 'заполните поле пароль1'})
    password2 = serializers.CharField(required=True, write_only=True,
                                      error_messages={'blank': 'заполните поле пароль2'})

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    {"email": "пользователь с таким email уже существует"})

        return email

    def validate_username(self, username):
        if User.objects.filter(username__exact=username).first():
            raise serializers.ValidationError(
                {"username": "пользователь с таким именем уже существует"})
        return get_adapter().clean_username(username)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "пароли не совпадают"})
        elif len(data['password1']) < 3 or len(data['password2']) < 3:
            raise serializers.ValidationError(
                {"password": "пароль  должен быть не меньше 3 символов"})
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


# МОЙ СЕРИАЛИЗАТОР ДЛЯ СОБЫТИЙ
class EventSerializer(serializers.ModelSerializer):
    # event_date = serializers.DateTimeField(format="%H:%M:%S || %d-%m-%Y",)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'author')
