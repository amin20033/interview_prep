from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path("register/",views.RegisterView.as_view()),
    path("login/",TokenObtainPairView.as_view(),name="login"),
    path("refresh/",TokenRefreshView.as_view()),
    path("resetrequest/",views.ForgotPasswordRequestView.as_view()),
    path("reset/<uidb64>/<token>/",views.ForgotPasswordSuccessView.as_view(),name="forgot-password-success"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("history/",views.HistoryView.as_view()),
    path("details/<int:id>/",views.DetailView.as_view())
]
