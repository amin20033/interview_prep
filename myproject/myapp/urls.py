from django.urls import path
from myapp import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    path("home/",views.home),
    path("signup/",views.signup),
    path("",views.userLogin),
    path("logout/",views.userLogout),
    path('password_reset/',
         PasswordResetView.as_view(),
         name='password_reset'),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path("history/",views.history),
    path("details/<int:id>/",views.details)
]
