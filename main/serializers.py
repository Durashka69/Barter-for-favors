from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from main.models import (
    Favor, Raiting, User, Category,
    Request_Favor, Subcategory,
)

from main.tasks import send_mail_to_email


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'title', 'description', 'category')


class RaitingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Raiting
        fields = ('id', 'user', 'username',
                  'favor', 'comment', 'score')

    def create(self, validated_data):
        raiting = Raiting.objects.filter(
            user=validated_data.get('user'), favor=validated_data.get('favor')
        ).first()
        if raiting:
            raiting.score = validated_data.get('score')
            if not raiting.comment:
                raiting.comment = validated_data.get('comment')
            raiting.save()
            return raiting
        raiting = Raiting.objects.create(user=validated_data.get(
            'user'), favor=validated_data.get('favor'), score=validated_data.get('score'), comment=validated_data.get('comment'))
        return raiting


class FavorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    # subcategory = SubcategorySerializer(read_only=True)
    subcategory_title = serializers.ReadOnlyField(source='subcategory.title')
    raiting = RaitingSerializer(read_only=True, many=True)

    class Meta:
        model = Favor
        fields = (
            'user', 'username',
            'id', 'title', 'description',
            'photo', 'favor_raiting',
            'sum_raiting', 'subcategory',
            'raiting', 'subcategory_title',
        )

        extra_kwargs = {
            'category': {'write_only': True},
            'subcategory': {'write_only': True},
            'user': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    r_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'r_password')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        r_password = attrs.get('r_password')
        if len(password) < 6:
            raise exceptions.ValidationError(
                {"error": "password is too short"})
        elif len(password) > 20:
            raise exceptions.ValidationError({"error": "password is too long"})
        elif password != r_password:
            raise exceptions.ValidationError(
                {"error": "passwords don`t match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            username=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key})


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'subcategory',)


class Request_FavorSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Request_Favor
        fields = (
            'id', 'user', 'username', 'favor', 'email',
            'date_created', 'content'
        )
        read_only_fields = ('date_created', 'user')

    def create(self, validated_data):
        print(validated_data)
        user = validated_data['user']
        favor = validated_data['favor']
        send_mail_to_email.delay(
            user.username,
            validated_data['email'],
            favor.title,
            validated_data['content'],
        )
        return super().create(validated_data)
