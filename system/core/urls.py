from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeRenderer, name="index-page"),
    path("explore/", views.exploreRenderer, name="explore-page"),
    path("about/", views.aboutRenderer, name="about-page"),
    path("contact/", views.contactRenderer, name="contact-page"),
    path("pet/<int:transaction_id>", views.petDetailsRenderer, name="pet-details-page"),
    path("profile/<int:user_id>", views.profileRenderer, name="profile-page"),
    path("request-delete/<int:request_id>", views.deleteReqest, name="request-delete-page"),
    path("transaction-delete/<int:transaction_id>", views.transactionDeleter, name="transaction-delete-page"),
    path("login/", views.user_login, name='login-page'),
    path("register/", views.register, name="registration-page"),
    path("logout/", views.user_logout, name="logout"),
    path('transaction-closing/<int:transaction_id>', views.transactionAcceptedAndClosed, name="transaction-closing-page")
]