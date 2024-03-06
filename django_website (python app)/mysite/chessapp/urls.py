from django.urls import path, include
from django.contrib.auth import views as auth_views



from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(next_page='/')),
    #path("signup/", views.signup, name="signup")
]