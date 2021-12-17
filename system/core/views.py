from django.shortcuts import render
from .models import * 
from django.contrib import messages

# Create your views here.
TEMPLATE_MAPPING = {
    "home-page": "index.html",
    "explore-page": "explore.html",
    "about-page": "about.html",
    "contact-page": "contact.html",
    "pet-details": "petDetails.html",
    "profile-page": "profile.html",
}

def homeRenderer(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["home-page"])


def exploreRenderer(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["explore-page"], context={"objects": Transaction.objects.all()})


def aboutRenderer(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["about-page"])


def contactRenderer(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["contact-page"])
    
    elif request.method == "POST":
        name = request.POST.get("w3lName")
        email = request.POST.get("w3lSender")
        issue = request.POST.get("w3lSubect")
        phonenumber = request.POST.get("w3lPhone")
        query = request.POST.get("w3lMessage")
        Queries.objects.create(name=name, email=email, issue=issue, phone=phonenumber, query=query)
        messages.add_message(request, messages.SUCCESS, "Query has been sent !")
        return render(request, TEMPLATE_MAPPING["contact-page"])


def petDetailsRenderer(request, transaction_id):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["pet-details"], context={"pet": Transaction.objects.get(id=transaction_id)})


def profileRenderer(request, user_id):
    if request.method == "GET":
        if request.user.id == user_id:
            return render(request, TEMPLATE_MAPPING["profile-page"], context={"is_self": True, "profile": User.objects.get(id=request.user.id)})
        
        else:
            return render(request, TEMPLATE_MAPPING["profile-page"], context={"is_self": False, "profile": User.objects.get(id=request.user.id)})