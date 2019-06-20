from rest_framework import serializers
from main_app.models import Game, Genre, Platform, Screenshot, Cover, Must, UserModel


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'cover', 'rating', 'version_title', 'platforms', 'genres',
                  'aggregated_rating', 'summary', 'first_release_date', 'rating_count',
                  'aggregated_rating_count', 'screenshots')


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = ('id', 'game', 'url')


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ('id', 'game', 'url')


class MustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Must
        fields = ('id', 'game', 'user', 'is_deleted')


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = UserModel.objects.create_user(**validated_data)
        return instance

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'gender', 'birthday')
