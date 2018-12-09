from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from . import views

router = routers.DefaultRouter()
router.register('user', views.UserView)
router.register('profile', views.ProfileView)
router.register('offer', views.OfferView)
router.register('comment',views.CommentView)
router.register('comment-response',views.CommentResponseView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/update-password/<int:id>',views.UpdatePasswordView),
    path('api/simple-profile/<int:pk>',views.SimpleProfileView.as_view())
  #  path(r'^authenticate/', CustomObtainAuthToken.as_view()),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
