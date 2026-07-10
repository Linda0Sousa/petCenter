from email.mime import image
from urllib import request

from django.shortcuts import render
from .forms import *
from .models import *
from .services import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
import json

#django does not has a decorator for inactive users ._.
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta

#in here is made email verification and is where user is activated
def verify_code(request, email):
    user = get_object_or_404(User, email=email)

    if user.is_active:
        return redirect("index")

    #in order to no resend and spam like crazy
    if request.method == 'GET':
        verification = EmailVerification.objects.filter(email=email).first()

        if verification and timezone.now() - verification.created_at < timedelta(seconds=30):
            pass
        else:
            send_verification_email(email)

    if request.method == 'POST':
        input_code = request.POST.get('code', '').strip()

        verification = EmailVerification.objects.filter(email=email).first()

        if not verification:
            return render(request, 'center/codeVerifcation.html', {
                'error': 'Code not found'
            })

        # Expiration 
        if timezone.now() - verification.created_at > timedelta(minutes=5):
            verification.delete()
            return render(request, 'center/codeVerifcation.html', {
                'error': 'code expired'
            })

        # Code check
        
        if input_code == verification.code:
            user.is_active = True
            user.save()

            verification.delete()

            return redirect("index")

        else:
            return render(request, 'center/codeVerifcation.html', {
                'error': 'Wrong code.'
            })

    return render(request, 'center/codeVerifcation.html')

#landing page and sign up
def index(request):
    SignUpForm = SignUp()

    if request.method == 'POST':
        SignUpForm = SignUp(request.POST)
        if SignUpForm.is_valid():

            user = SignUpForm.save()
            assign_client_group(user)

            email = SignUpForm.cleaned_data['email']
            
            
            return render(request, "center/codeVerifcation.html", {"email" : email})
    
        else:
            return HttpResponse(SignUpForm.errors)

    return render(request, 'center/landing.html', {"SignUpForm"  : SignUpForm})

#login form
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(username=username)
        
            if not user_obj.is_active:
                return redirect("verify_code", email=user_obj.email)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("feed")
            
        except:
            return render(request, "center/login.html", {"error": "Invalid credentials"})

    return render(request, "center/login.html")

#all animals listed in the feed
def feed(request):
    animals = Pet.objects.all()

    for animal in animals:
        animal.main_image = PetImage.objects.filter(pet=animal).first()

    return render(request, "center/feed.html", {"animals": animals})

#create a pet
#@permission_required('center.add_pet', raise_exception=True)
def create_pet(request):

    Form = CreatePet()

    if request.method == "POST":
        Form = CreatePet(request.POST)

        if Form.is_valid():
            pet = Form.save()

            image = request.FILES.get("main_image")
            images = request.FILES.getlist("images")
            
            array = list(images)

            if image:
                array.insert(0, image)

            if not image:
                raise ValueError("You need at least one image")

            if len(array) > 6:
                pet.delete()
                raise ValueError("Maximum of 6 images")
            
            for img in array:
                PetImage.objects.create(pet=pet, image=img)


    return render(request, "center/createPet.html", {
        "form": Form,
    })

#see pet
def see_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet_images = PetImage.objects.filter(pet=pet)
    return render(request, "center/seePet.html", {
        "pet": pet,
        "pet_images": pet_images,
    })

#dashboard
def dashboard(request):
    return render(request, "center/dashboard.html")

#profile for clients/it needs also to check if its a client. it might be more secure to make a diferent view for that than using the same one.
#it also needs to send code for email
@login_required
def profile(request):

    if request.method == "POST":

        data = json.loads(request.body)

        current_email = request.user.email

        email = data.get("email")
        phone = data.get("phone")

        request.user.email = email
        request.user.phone_number = phone

        try:
            request.user.full_clean()

            #quickly saves if email is the same
            if current_email == email:
                request.user.save()
                return JsonResponse({
                    "success": True,
                    "message": "Profile updated successfully."
                })

            else:
                
                #if email change sends code
                send_verification_email(email)

                #code verification
                result, message = verify_code(request, email)

                return JsonResponse({
                    "success": result,
                    "message": message,
                }) 
         
        except ValidationError as e:
            return JsonResponse({
                "success": False,
                "errors": e.message_dict
            }, status=400)

    return render(request, "center/profile.html", {"user": request.user})

#list of requests for the shelter
def requests(request):
    return render(request, "center/requests.html")


#logout
@login_required
def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect("index")