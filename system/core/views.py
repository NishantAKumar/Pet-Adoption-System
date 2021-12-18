from django.shortcuts import redirect, render
from django.utils import tree
from .models import * 
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

# Create your views here.
TEMPLATE_MAPPING = {
    "home-page": "index.html",
    "explore-page": "explore.html",
    "about-page": "about.html",
    "contact-page": "contact.html",
    "pet-details": "petDetails.html",
    "profile-page": "profile.html",
    "login-page": "login.html",
    "registration-page": "register.html",
    "transaction-create-page" : "transactionCreate.html",
    "transaction-delete-page" : "transactionDelete.html",
    "request-delete-page" : "requestDelete.html",
    "transaction-closing-page": "transactionClosing.html"
}

def homeRenderer(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["home-page"])


def exploreRenderer(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["explore-page"], context={"objects": Transaction.objects.filter(accepted_req_id__isnull=True)})


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
    elif request.method == "POST":
        transaction = Transaction.objects.get(id=transaction_id)
        if request.user.id != transaction.donor_id.id:
            reason = request.POST.get("reason")
            applicant = User.objects.get(id=request.user.id)
            Request.objects.create(transaction_id=Transaction.objects.get(id=transaction_id), reason=reason, applicant_id=applicant)
            messages.add_message(request, messages.SUCCESS, "Request generated")
        else:
            messages.add_message(request, messages.ERROR, "You cannot request a pet from yourself")
        return render(request, TEMPLATE_MAPPING["pet-details"], context={"pet": Transaction.objects.get(id=transaction_id)})


def profileRenderer(request, user_id):
    if request.method == "GET":
        if request.user.id == user_id:
            return render(request, TEMPLATE_MAPPING["profile-page"], context={"is_self": True, "profile": User.objects.get(id=request.user.id), "requests": Request.objects.filter(applicant_id=request.user.id), "transactions": Transaction.objects.filter(donor_id=request.user.id, accepted_req_id__isnull=True)})
        else:
            return render(request, TEMPLATE_MAPPING["profile-page"], context={"is_self": False, "profile": User.objects.get(id=request.user.id)})


def deleteReqest(request, request_id):
    if request.method == "POST":
        Request.objects.get(id=request_id).delete()
        messages.add_message(
            request, 
            messages.SUCCESS,
            "Request Deleted"
        )
        return redirect(to=f"/profile/{request.user.id}")


def user_login(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["login-page"])
    
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, "Login Failed")
            return render(request, TEMPLATE_MAPPING["login-page"])
        
        login(request, user)

        return redirect(to="/")


def register(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["registration-page"])

    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        area = request.POST.get("area")
        city = request.POST.get("city")
        country = request.POST.get("country")
        phone = request.POST.get("phone")

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "User already exists!")
            return render(request, TEMPLATE_MAPPING["registration-page"])

        if User.objects.filter(email=email).exists():
            messages.add_message(
                request,
                messages.ERROR, 
                "Email already exists!"
                )
            return render(request, TEMPLATE_MAPPING["registration-page"])
        
        if password != confirm:
            messages.add_message(request, messages.ERROR, "Passwords do not match")
            return render(request, TEMPLATE_MAPPING["registration-page"])
        
        User.objects.create_user(
            username=username,
            password=password,
            email=email,
            area=area,
            city=city,
            country=country,
            phone=phone)
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, "Login Failed")
            return render(request, TEMPLATE_MAPPING["login-page"])
        
        login(request, user)

        return redirect("/")


def user_logout(request):
    if request.method == "GET" and request.user.is_authenticated:
        logout(request)
        return redirect("/")
    elif not request.user.is_authenticated:
        return redirect("/login")


def transactionCreator(request):
    if request.method == "GET":
        return render(request, TEMPLATE_MAPPING["transaction-create-page"])

    elif request.method == "POST":
        name = request.POST.get("w3lName")
        description = request.POST.get("w3lDesc")
        image = request.FILES.get("w3lImage")
        donor = User.objects.get(id=request.user.id)
        Transaction.objects.create(name=name, desc=description, img=image, donor_id=donor)
        messages.add_message(
            request, 
            messages.SUCCESS,
            "Transaction Created"
        )
        return render(request, TEMPLATE_MAPPING["transaction-create-page"])


def transactionDeleter(request, transaction_id):
    if request.method == "POST":
        Transaction.objects.get(id=transaction_id).delete()
        messages.add_message(
            request, 
            messages.SUCCESS,
            "Transaction Deleted"
        )
        return redirect(to=f"/profile/{request.user.id}")


def transactionAcceptedAndClosed(request, transaction_id):
    if request.method == "GET":
        applicant_requests = Request.objects.filter(transaction_id=transaction_id)
        return render(request, TEMPLATE_MAPPING["transaction-closing-page"], context={"applicants": applicant_requests})

    if request.method == "POST":
        request_id = request.POST.get("applicant")
        chosen_request = Request.objects.get(id=request_id)
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.accepted_req_id = chosen_request
        transaction.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Trasaction Completed and Closed"
        )

        return redirect(to=f"/profile/{request.user.id}")


# Todo:
# Html templates
# Regex
# Dark Mode check certain pages
# Navbar dynamic