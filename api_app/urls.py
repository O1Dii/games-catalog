from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from api_app.routers import HybridRouter
from .views import (GameRestView, PlatformRestView, GenreRestView,
                    CoverRestView, ScreenshotRestView, MustRestView, MustObjectRestView, Logout, ActivationView,
                    Registration, SendEmailAgain)

app_name = 'api_app'

router = HybridRouter(app_name)
router.register('games', GameRestView, basename='games')
router.register('platforms', PlatformRestView, basename='platforms')
router.register('genres', GenreRestView, basename='genres')
router.register('covers', CoverRestView, basename='covers')
router.register('screenshots', ScreenshotRestView, basename='screenshots')
router.add_api_view('musts', path('musts/', MustRestView.as_view(), name='musts'))
router.add_api_view('must', path('musts/<int:pk>/', MustObjectRestView.as_view(), name='must_object'))
router.add_api_view('logout', path('logout/', Logout.as_view(), name='logout'))
router.add_api_view('registration', path('registration/', Registration.as_view(), name='registration'))
router.add_api_view('activate', path('activate/<slug:uidb64>/<token:token>/', ActivationView.as_view(), name='activate'))
router.add_api_view('send_email', path('send_email/', SendEmailAgain.as_view(), name='send_again'))
router.add_api_view('login', path('login/', obtain_auth_token, name='login'))

urlpatterns = (
    path('', include(router.urls)),
)
