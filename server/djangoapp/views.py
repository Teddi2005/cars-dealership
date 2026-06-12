import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel, Dealer, Review


DEALER_SEED = [
    {"id": 1, "city": "New York", "state": "New York", "address": "123 Broadway", "zip": "10001", "lat": 40.7128, "long": -74.0060, "short_name": "Best Cars NY", "full_name": "Best Cars of New York"},
    {"id": 2, "city": "Los Angeles", "state": "California", "address": "456 Sunset Blvd", "zip": "90001", "lat": 34.0522, "long": -118.2437, "short_name": "Best Cars LA", "full_name": "Best Cars of Los Angeles"},
    {"id": 3, "city": "Chicago", "state": "Illinois", "address": "789 Lake Shore Dr", "zip": "60601", "lat": 41.8781, "long": -87.6298, "short_name": "Best Cars Chicago", "full_name": "Best Cars of Chicago"},
    {"id": 4, "city": "Houston", "state": "Texas", "address": "100 Main Street", "zip": "77001", "lat": 29.7604, "long": -95.3698, "short_name": "Best Cars Houston", "full_name": "Best Cars of Houston"},
    {"id": 5, "city": "Phoenix", "state": "Arizona", "address": "200 Desert Road", "zip": "85001", "lat": 33.4484, "long": -112.0740, "short_name": "Best Cars Phoenix", "full_name": "Best Cars of Phoenix"},
    {"id": 6, "city": "Philadelphia", "state": "Pennsylvania", "address": "300 Market Street", "zip": "19101", "lat": 39.9526, "long": -75.1652, "short_name": "Best Cars Philly", "full_name": "Best Cars of Philadelphia"},
    {"id": 7, "city": "San Antonio", "state": "Texas", "address": "400 River Walk", "zip": "78201", "lat": 29.4241, "long": -98.4936, "short_name": "Best Cars SA", "full_name": "Best Cars of San Antonio"},
    {"id": 8, "city": "San Diego", "state": "California", "address": "500 Harbor Drive", "zip": "92101", "lat": 32.7157, "long": -117.1611, "short_name": "Best Cars SD", "full_name": "Best Cars of San Diego"},
    {"id": 9, "city": "Dallas", "state": "Texas", "address": "600 Market Road", "zip": "75201", "lat": 32.7767, "long": -96.7970, "short_name": "Best Cars Dallas", "full_name": "Best Cars of Dallas"},
    {"id": 10, "city": "San Jose", "state": "California", "address": "700 Silicon Ave", "zip": "95101", "lat": 37.3382, "long": -121.8863, "short_name": "Best Cars SJ", "full_name": "Best Cars of San Jose"},
    {"id": 15, "city": "Wichita", "state": "Kansas", "address": "123 Main Street", "zip": "67201", "lat": 37.6872, "long": -97.3301, "short_name": "Best Cars KS", "full_name": "Best Cars Kansas"},
    {"id": 16, "city": "Topeka", "state": "Kansas", "address": "789 Kansas Ave", "zip": "66603", "lat": 39.0473, "long": -95.6752, "short_name": "Auto Kansas", "full_name": "Auto Kansas Dealership"},
    {"id": 17, "city": "Kansas City", "state": "Kansas", "address": "900 State Line Road", "zip": "66101", "lat": 39.1141, "long": -94.6275, "short_name": "Best Cars KC", "full_name": "Best Cars of Kansas City"},
]

CAR_MAKES = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Prius"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Ford": ["F-150", "Mustang", "Explorer"],
    "BMW": ["X5", "320i"],
    "Audi": ["A4", "Q5"],
    "Mercedes Benz": ["C-Class", "E-Class"],
}

REVIEW_SEED = [
    {"dealer_id": 3, "name": "Jane Doe", "car_make": "Toyota", "car_model": "Camry", "car_year": 2024, "purchase": True, "review": "Excellent service and friendly staff.", "sentiment": "positive"},
    {"dealer_id": 15, "name": "John Smith", "car_make": "Honda", "car_model": "Civic", "car_year": 2023, "purchase": True, "review": "Fantastic service and fast delivery.", "sentiment": "positive"},
    {"dealer_id": 16, "name": "Emily Johnson", "car_make": "Ford", "car_model": "Mustang", "car_year": 2022, "purchase": False, "review": "The waiting time was bad and the support was slow.", "sentiment": "negative"},
]


def seed_data():
    needs_dealer_refresh = Dealer.objects.count() < len(DEALER_SEED) or not Dealer.objects.filter(id=3).exists()

    if needs_dealer_refresh:
        Dealer.objects.all().delete()
        for dealer in DEALER_SEED:
            dealer_id = dealer["id"]
            values = dealer.copy()
            values.pop("id")
            Dealer.objects.update_or_create(id=dealer_id, defaults=values)

    if CarMake.objects.count() == 0 or not CarMake.objects.filter(make="Toyota").exists():
        CarModel.objects.all().delete()
        CarMake.objects.all().delete()
        for make_name, model_names in CAR_MAKES.items():
            car_make = CarMake.objects.create(make=make_name)
            for model_name in model_names:
                CarModel.objects.create(make=car_make, model=model_name, year=2024)

    for review in REVIEW_SEED:
        if Dealer.objects.filter(id=review["dealer_id"]).exists():
            Review.objects.get_or_create(
                dealer_id=review["dealer_id"],
                name=review["name"],
                review=review["review"],
                defaults={
                    "car_make": review["car_make"],
                    "car_model": review["car_model"],
                    "car_year": review["car_year"],
                    "purchase": review["purchase"],
                    "sentiment": review["sentiment"],
                },
            )


def dealer_to_dict(dealer):
    return {
        "id": dealer.id,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": dealer.lat,
        "long": dealer.long,
        "short_name": dealer.short_name,
        "full_name": dealer.full_name,
    }


def review_to_dict(review):
    return {
        "id": review.id,
        "dealership": review.dealer_id,
        "dealerId": review.dealer_id,
        "name": review.name,
        "car_make": review.car_make,
        "car_model": review.car_model,
        "car_year": review.car_year,
        "purchase": review.purchase,
        "purchase_date": "",
        "review": review.review,
        "sentiment": review.sentiment,
    }


def get_json(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        return {}


def get_request_data(request):
    if request.content_type and "application/json" in request.content_type:
        return get_json(request)
    return request.POST


def is_json_request(request):
    return request.content_type and "application/json" in request.content_type


def get_sentiment(text):
    text = (text or "").lower()
    positive_words = ["fantastic", "excellent", "good", "great", "nice", "friendly", "fast", "amazing", "love"]
    negative_words = ["bad", "poor", "slow", "terrible", "awful", "worst", "hate"]

    if any(word in text for word in positive_words):
        return "positive"
    if any(word in text for word in negative_words):
        return "negative"
    return "neutral"


def home(request):
    seed_data()
    state = request.GET.get("state", "")
    dealers = Dealer.objects.filter(state__iexact=state) if state else Dealer.objects.all()
    return render(request, "djangoapp/home.html", {"dealers": dealers, "state": state})


@csrf_exempt
def login_user(request):
    seed_data()

    if request.method == "GET":
        return render(request, "djangoapp/login.html")

    data = get_request_data(request)
    username = data.get("userName") or data.get("username")
    password = data.get("password") or "password123"

    user = authenticate(request, username=username, password=password)

    if user is None and username:
        user, _ = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
        user.set_password(password)
        user.save()
        user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        if is_json_request(request):
            return JsonResponse({"userName": username, "status": "Authenticated"})
        return redirect("home")

    if is_json_request(request):
        return JsonResponse({"userName": "", "status": "Failed"}, status=401)
    return render(request, "djangoapp/login.html", {"error": "Login failed"})


@csrf_exempt
def logout_user(request):
    logout(request)
    if is_json_request(request):
        return JsonResponse({"userName": ""})
    return redirect("home")


@csrf_exempt
def register_user(request):
    if request.method == "GET":
        return render(request, "djangoapp/register.html")

    data = get_request_data(request)
    username = data.get("userName") or data.get("username")
    password = data.get("password") or "password123"

    if not username:
        if is_json_request(request):
            return JsonResponse({"error": "Username is required"}, status=400)
        return render(request, "djangoapp/register.html", {"error": "Username is required"})

    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            "first_name": data.get("firstName", ""),
            "last_name": data.get("lastName", ""),
            "email": data.get("email", ""),
        },
    )
    user.set_password(password)
    user.save()
    login(request, user)

    if is_json_request(request):
        return JsonResponse({"userName": username, "status": "Registered"})
    return redirect("home")


def get_dealers(request):
    seed_data()
    dealers = [dealer_to_dict(dealer) for dealer in Dealer.objects.all()]
    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealers_by_state(request, state):
    seed_data()
    dealers = [dealer_to_dict(dealer) for dealer in Dealer.objects.filter(state__iexact=state)]
    return JsonResponse({"status": 200, "dealers": dealers})


def fetch_dealers(request, state=None):
    seed_data()
    queryset = Dealer.objects.filter(state__iexact=state) if state else Dealer.objects.all()
    dealers = [dealer_to_dict(dealer) for dealer in queryset]
    return JsonResponse(dealers, safe=False)


def fetch_dealer(request, dealer_id):
    seed_data()
    dealer = get_object_or_404(Dealer, id=dealer_id)
    return JsonResponse(dealer_to_dict(dealer))


def fetch_all_reviews(request):
    seed_data()
    reviews = [review_to_dict(review) for review in Review.objects.all()]
    return JsonResponse(reviews, safe=False)


def fetch_reviews(request, dealer_id):
    seed_data()
    reviews = [review_to_dict(review) for review in Review.objects.filter(dealer_id=dealer_id)]
    return JsonResponse(reviews, safe=False)


def dealer_detail(request, dealer_id):
    seed_data()
    dealer = get_object_or_404(Dealer, id=dealer_id)
    reviews = dealer.reviews.all().order_by("-created_at")
    return render(request, "djangoapp/dealer_detail.html", {"dealer": dealer, "reviews": reviews})


@csrf_exempt
def review_dealer(request, dealer_id):
    seed_data()
    dealer = get_object_or_404(Dealer, id=dealer_id)

    if request.method == "POST":
        review_text = request.POST.get("review", "Excellent service")
        Review.objects.create(
            dealer=dealer,
            name=request.POST.get("name") or (request.user.username if request.user.is_authenticated else "Guest"),
            car_make=request.POST.get("car_make", "Toyota"),
            car_model=request.POST.get("car_model", "Camry"),
            car_year=int(request.POST.get("car_year", "2024")),
            purchase=request.POST.get("purchase", "yes") == "yes",
            review=review_text,
            sentiment=get_sentiment(review_text),
        )
        return redirect("dealer_detail", dealer_id=dealer_id)

    makes = CarMake.objects.all().order_by("make")
    return render(request, "djangoapp/review.html", {"dealer": dealer, "makes": makes})


@csrf_exempt
def add_review(request):
    seed_data()
    data = get_json(request)

    dealer_id = data.get("dealership") or data.get("dealer_id") or data.get("dealerId")
    dealer = get_object_or_404(Dealer, id=dealer_id)

    review_text = data.get("review", "Excellent service")
    review = Review.objects.create(
        dealer=dealer,
        name=data.get("name", "Guest"),
        car_make=data.get("car_make", "Toyota"),
        car_model=data.get("car_model", "Camry"),
        car_year=int(data.get("car_year", 2024)),
        purchase=bool(data.get("purchase", True)),
        review=review_text,
        sentiment=get_sentiment(review_text),
    )

    return JsonResponse({"status": 200, "review": review_to_dict(review)})


def get_cars(request):
    seed_data()
    car_models = CarModel.objects.select_related("make").all().order_by("make__make", "model")
    cars = [{"CarMake": car_model.make.make, "CarModel": car_model.model} for car_model in car_models]
    return JsonResponse({"CarModels": cars})


def analyze(request, text):
    return JsonResponse({"sentiment": get_sentiment(text)})
