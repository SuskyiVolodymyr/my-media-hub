from django.urls import path

from media.views import index

urlpatterns = [
    path("", index, name="index")
]

app_name = "media"
