import json
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

import ssl, urllib.request
from urllib.parse import quote
from random import randint


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "composers/login.html", {
                "message": "Invalid username and/ or password."
            })
    else:
        return render(request, "composers/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Ensure password matches confirmation
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "composers/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "composers/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "composers/register.html")

#==================================================================================
def index(request):
    # init_db_from_epochs_data()
    # init_db_from_data_dump()

    epochs = Epoch.objects.all()
    genres = Genre.objects.all()
    epoch_composers_dict = dict()
    for epoch in epochs:
        epoch_composers_dict[epoch] = Composer.objects.filter(epoch=epoch).order_by("birth", "death")

    return render(request, "composers/index.html", {
        "epochs": epochs,
        "genres": genres,
        "epoch_composers_dict": epoch_composers_dict
    })


def init_db_from_epochs_data():
    epochs = get_or_create_epochs()

    for epoch in epochs:
        epoch_encoded = quote(epoch.epoch)
        url = f"https://api.openopus.org/composer/list/epoch/{epoch_encoded}.json"
        data = load_api_data_from_url(url)
        epoch_composers = data["composers"]
        get_or_create_epoch_composer(epoch, epoch_composers)


def get_or_create_epochs():
    epoch_names = ["Medieval", "Renaissance", "Baroque", "Classical", "Early Romantic", "Romantic", "Late Romantic", "20th Century", "Post-War", "21st Century"]

    for epoch_name in epoch_names:
        epoch, created = Epoch.objects.get_or_create(epoch=epoch_name)

    epochs = Epoch.objects.all()
    return epochs


def get_or_create_epoch_composer(epoch, epoch_composers):
        for epoch_composer in epoch_composers:
            # Parse birth and death date
            birth_obj = datetime.strptime(epoch_composer["birth"], "%Y-%m-%d")
            epoch_composer["birth"] = birth_obj
            if epoch_composer["death"] == None:
                epoch_composer["death"] = None
            else: 
                death_obj = datetime.strptime(epoch_composer["death"], "%Y-%m-%d")
                epoch_composer["death"] = death_obj

            composer, created = Composer.objects.get_or_create(
                composer_id = epoch_composer["id"],
                name = epoch_composer["name"],
                complete_name = epoch_composer["complete_name"],
                epoch = epoch,
                birth = epoch_composer["birth"],
                death = epoch_composer["death"],
                portrait = epoch_composer["portrait"]
            )
            composer.save()


def init_db_from_data_dump():
    url = "https://api.openopus.org/work/dump.json"
    data_dump = load_api_data_from_url(url)
    data_dump_composers = data_dump["composers"]

    for data_dump_composer in data_dump_composers:
        composer = Composer.objects.filter(
            complete_name=data_dump_composer["complete_name"],
            epoch = Epoch.objects.filter(epoch=data_dump_composer["epoch"]).first()
        ).first()

        if composer != None:
            update_composer_recommended(data_dump_composer, composer)
            get_or_create_composer_works(data_dump_composer, composer)


def update_composer_recommended(dump_composer, composer):
    composer.is_popular = dump_composer["popular"]
    composer.is_recommended = dump_composer["recommended"]
    composer.save()


def get_or_create_composer_works(dump_composer, composer):
    works = dump_composer["works"]

    for work in works:
        genre, created = Genre.objects.get_or_create(genre=work["genre"])
        composer.genres.add(genre)

        work_obj, created = Work.objects.get_or_create(
            title = work["title"],
            is_popular = work["popular"],
            is_recommended = work["recommended"],
            genre = genre,
            composer = composer
        )
        work_obj.save()


def load_api_data_from_url(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(url).read()
    data = json.loads(response)

    return data
    

def composer(request, composer_id):
    composer = Composer.objects.get(composer_id=composer_id)
    works = Work.objects.filter(composer=composer)
    genres = composer.genres.all()

    if request.user.is_authenticated:
        user_likes = Like.objects.filter(user=request.user)
        user_liked_works = [like.work for like in user_likes]
    else:
        user_liked_works = None

    return render(request, "composers/composer.html", {
        "composer": composer,
        "genres": genres,
        "works": works,
        "user_liked_works": user_liked_works
    })


def discover(request):
    num_of_composers = len(Composer.objects.all())
    random_composer = Composer.objects.all()[randint(0, num_of_composers - 1)]
    random_composer_id = random_composer.composer_id

    return HttpResponseRedirect(reverse("composer", args=(random_composer_id,)))


def favorites(request):
    if not request.user.is_authenticated:
        return render(request, "composers/login.html", {
            "message": """Please log in to access the "Favorites" page."""
        })
    
    user_likes = Like.objects.filter(user=request.user).order_by("-liked_date_time")
    user_liked_works = [like.work for like in user_likes]

    return render(request, "composers/favorites.html", {
        "user_liked_works": user_liked_works
    })

#==================================================================================
# API

@csrf_exempt
@login_required
def api_work(request, work_id):
    try:
        work = Work.objects.get(pk=work_id)
    except:
        return JsonResponse({"error": "Work not found."}, status=404)

    if request.method == "GET":
        pass

    # Update like backend
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("current_user") is not None:
            current_user = User.objects.get(username=data["current_user"])
            toggle_like_status(current_user, work)
            # update_liked_date_time(work)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required"
        }, status=400)


def toggle_like_status(current_user, work):
    liked_works_ids = current_user.all_likes.all().values_list('work', flat='true')

    if work.pk in liked_works_ids:
        Like.objects.get(work=work).delete()
    else:
        like = Like.objects.create(
            user = current_user,
            work = work
        )
        like.save() 

    # if liked_works_ids.contains(work):
    #     current_user.favorites.remove(work)
    # else:
    #     current_user.favorites.add(work)
    # current_user.save() 


# def update_liked_date_time(work):
#     work.liked_date_time = datetime.now()
#     work.save()