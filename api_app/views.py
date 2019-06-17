from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_app.serializers import (GameSerializer, PlatformSerializer, GenreSerializer, CoverSerializer,
                                 ScreenshotSerializer, MustSerializer, UserSerializer)
from main_app.models import Platform, Genre, Cover, Screenshot, Must, UserModel, Game
from main_app.utils import search_in_queryset, auth_token_check, send_email
from main_app.views import GamesFilteredQuerysetMixin


class GameRestView(GamesFilteredQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)


class PlatformRestView(viewsets.ModelViewSet):
    serializer_class = PlatformSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = search_in_queryset(Platform.objects.all(), search)
        return queryset


class GenreRestView(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = search_in_queryset(Genre.objects.all(), search)
        return queryset


class CoverRestView(viewsets.ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer
    permission_classes = (IsAuthenticated,)


class ScreenshotRestView(viewsets.ModelViewSet):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer
    permission_classes = (IsAuthenticated,)


class MustRestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Must.objects.all()
        if queryset:
            serializer = MustSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response([])

    def post(self, request):
        game_id = int(request.data['game_id'])
        user = request.user.id
        try:
            Must.objects.get_or_create(game=Game.objects.get(id=game_id), user=user)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class MustObjectRestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Must.objects.get(pk=pk)
        except Must.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        must = self.get_object(pk)
        serializer = MustSerializer(must)
        return Response(serializer.data)

    def put(self, request, pk):
        must = self.get_object(pk)
        data = {k: v for k, v in request.data.items()}
        data['user'] = request.user.id
        serializer = MustSerializer(must, data=data)
        if serializer.is_valid():
            try:
                Must.objects.get(game=Game.objects.get(id=int(data['game'])),
                                 user=request.user)
                return Response(status=status.HTTP_409_CONFLICT)
            except Must.DoesNotExist:
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete(force=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            send_email(request, user, True)
            return Response('Verification email has been sent to you mail')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailAgain(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return Response('Bad email', status=status.HTTP_400_BAD_REQUEST)
            else:
                if user.is_active:
                    return Response('User already activated')
                else:
                    send_email(request, user, True)
                    return Response(f'Email has been sent to {email}')
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        if not request.user.is_anonymous:
            request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivationView(View):
    def get(self, request, uidb64, token):
        user = auth_token_check(uidb64, token)
        if user:
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse_lazy('main_app:main_page'))
        else:
            return redirect(reverse_lazy('main_app:send_email'))
