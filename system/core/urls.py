from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeRenderer, name="index-page"),
    path("explore/", views.exploreRenderer, name="explore-page"),
    path("about/", views.aboutRenderer, name="about-page"),
    path("contact/", views.contactRenderer, name="contact-page"),
    path("pet/<int:transaction_id>", views.petDetailsRenderer, name="pet-details-page"),
    path("profile/<int:user_id>", views.profileRenderer, name="profile-page")
]