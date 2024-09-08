from django.urls import path, include
from django.contrib.auth import views as auth_views



from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_view, name="logout_view"),
    path("login/", auth_views.LoginView.as_view(next_page='/')),
    path('save_image/', views.save_image, name='save_image'),
    path("analysis/", views.analysis, name='analysis'),
    #path("signup/", views.signup, name="signup")
]