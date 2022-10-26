from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("composer/<int:composer_id>", views.composer, name="composer"),
    path("discover", views.discover, name="discover"),
    path("favorites", views.favorites, name="favorites"),

    # API
    path("api/work/<int:work_id>", views.api_work, name="api_work")
]