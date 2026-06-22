from django.urls import path, include
from . import views
urlpatterns = [
  path("hello/",views.HelloAPIView.as_view())
]