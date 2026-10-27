from django.urls import path

from . import views

urlpatterns = [
    path("homepage/", views.homepage),
    path("titles/<int:pk>/", views.title_detail),
    path("search/", views.search),
]
