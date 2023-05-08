from django.contrib import admin
from django.urls import path
from ads.views.cat import *

urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:pk>/", CategoryDetailView.as_view()),
    path("create/", CategoryCreateView.as_view()),
    path("<int:pk>/update/", CategoryCreateView.as_view()),
    path("<int:pk>/delete/", CategoryDeleteView.as_view()),

]