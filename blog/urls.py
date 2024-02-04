
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="blogHome"),
    path("myblogposts/<int:id>", views.blogpost)
]