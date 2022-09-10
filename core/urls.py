from django.urls import path
from .views import MyObtainTokenPairView,RegisterView,ListUserView, UpdateProfile,UpdateProfileView,UpdateUserPasswordView,DeleteAccount,ProfileListView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='register'),
    path('list', ListUserView.as_view(), name='list'),
    path('profile', ProfileListView.as_view(), name='profile'),
    path('update/<int:pk>', UpdateProfile.as_view(), name='update'),
    path('change_password/<int:pk>', UpdateUserPasswordView.as_view(), name='password'),
    path('delete_account/<int:pk>', DeleteAccount.as_view(), name='delete')
]