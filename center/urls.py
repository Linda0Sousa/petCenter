from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("verify/<str:email>/", views.verify_code, name="verify_code"),
    path("feed/", views.feed, name="feed"),
    path("create_pet/", views.create_pet, name="create_pet"),
    path("see_pets/", views.see_pets, name="see_pets"),
]