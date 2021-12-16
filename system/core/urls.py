from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeRenderer, name="index-page"),
    path("explore/", views.exploreRenderer, name="explore-page"),
    path("about/", views.aboutRenderer, name="about-page"),
    path("contact/", views.contactRenderer, name="contact-page"),
    path("pet/", views.petDetailsRenderer, name="pet-details-page"),
]