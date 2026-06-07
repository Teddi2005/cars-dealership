import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer, Review, CarMake, CarModel


def seed_data():
    if Dealer.objects.exists():
        return
    dealers = [
        (1,'New York','New York','123 Broadway','10001',40.7128,-74.0060,'Best Cars NY','Best Cars of New York'),
        (2,'Los Angeles','California','456 Sunset Blvd','90001',34.0522,-118.2437,'Best Cars LA','Best Cars of Los Angeles'),
        (15,'Wichita','Kansas','123 Main Street','67201',37.6872,-97.3301,'Best Cars KS','Best Cars Kansas'),
        (16,'Topeka','Kansas','789 Kansas Ave','66603',39.0473,-95.6752,'Auto Kansas','Auto Kansas Dealership'),
        (20,'Dallas','Texas','500 Market Road','75201',32.7767,-96.7970,'Best Cars TX','Best Cars Texas'),
    ]
    for d in dealers:
        Dealer.objects.create(id=d[0], city=d[1], state=d[2], address=d[3], zip=d[4], lat=d[5], long=d[6], short_name=d[7], full_name=d[8])
    makes = {'Toyota':['Camry','Corolla','RAV4'], 'Audi':['A4','Q5'], 'BMW':['X5','320i'], 'Honda':['Civic','Accord']}
    for make, models in makes.items():
        cm = CarMake.objects.create(make=make)
        for model in models:
            CarModel.objects.create(make=cm, model=model, year=2024)
    Review.objects.create(dealer_id=15, name='John Smith', car_make='Toyota', car_model='Camry', car_year=2024, purchase=True, review='Fantastic services', sentiment='positive')


def dealer_to_dict(d):
    return {'id': d.id, 'city': d.city, 'state': d.state, 'address': d.address, 'zip': d.zip, 'lat': d.lat, 'long': d.long, 'short_name': d.short_name, 'full_name': d.full_name}

def review_to_dict(r):
    return {'id': r.id, 'dealerId': r.dealer_id, 'name': r.name, 'car_make': r.car_make, 'car_model': r.car_model, 'car_year': r.car_year, 'purchase': r.purchase, 'review': r.review, 'sentiment': r.sentiment}

def get_json(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except Exception:
        return {}


def home(request):
    seed_data()
    state = request.GET.get('state', '')
    dealers = Dealer.objects.filter(state__iexact=state) if state else Dealer.objects.all()
    return render(request, 'djangoapp/home.html', {'dealers': dealers, 'state': state})

@csrf_exempt
def login_user(request):
    seed_data()
    data = get_json(request)
    username = data.get('userName') or data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is None and username and password:
        user, _ = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
        user.set_password(password)
        user.save()
        user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'userName': username, 'status': 'Authenticated'})
    return JsonResponse({'userName': '', 'status': 'Failed'}, status=401)

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({'userName': ''})

@csrf_exempt
def register_user(request):
    data = get_json(request)
    username = data.get('userName') or data.get('username')
    password = data.get('password') or 'password123'
    user, created = User.objects.get_or_create(username=username, defaults={'first_name': data.get('firstName',''), 'last_name': data.get('lastName',''), 'email': data.get('email','')})
    user.set_password(password)
    user.save()
    return JsonResponse({'userName': username, 'status': 'Registered'})

def get_dealers(request):
    seed_data()
    return JsonResponse({'dealers': [dealer_to_dict(d) for d in Dealer.objects.all()]})

def get_dealers_by_state(request, state):
    seed_data()
    return JsonResponse({'dealers': [dealer_to_dict(d) for d in Dealer.objects.filter(state__iexact=state)]})

def fetch_dealers(request):
    return get_dealers(request)

def fetch_dealers_state(request, state):
    return get_dealers_by_state(request, state)

def fetch_dealer(request, dealer_id):
    seed_data()
    d = get_object_or_404(Dealer, id=dealer_id)
    return JsonResponse(dealer_to_dict(d))

def fetch_reviews(request, dealer_id):
    seed_data()
    return JsonResponse({'dealerId': dealer_id, 'reviews': [review_to_dict(r) for r in Review.objects.filter(dealer_id=dealer_id)]})

def dealer_detail(request, dealer_id):
    seed_data()
    dealer = get_object_or_404(Dealer, id=dealer_id)
    return render(request, 'djangoapp/dealer_detail.html', {'dealer': dealer, 'reviews': dealer.reviews.all()})

@csrf_exempt
def review_dealer(request, dealer_id):
    seed_data()
    dealer = get_object_or_404(Dealer, id=dealer_id)
    if request.method == 'POST':
        Review.objects.create(
            dealer=dealer,
            name=request.POST.get('name') or (request.user.username if request.user.is_authenticated else 'Guest'),
            car_make=request.POST.get('car_make','Toyota'),
            car_model=request.POST.get('car_model','Camry'),
            car_year=int(request.POST.get('car_year','2024')),
            purchase=request.POST.get('purchase','yes') == 'yes',
            review=request.POST.get('review','Excellent service'),
            sentiment='positive'
        )
        return redirect('dealer_detail', dealer_id=dealer_id)
    return render(request, 'djangoapp/review.html', {'dealer': dealer})

def get_cars(request):
    seed_data()
    models = [{'make': m.make.make, 'model': m.model, 'year': m.year} for m in CarModel.objects.select_related('make').all()]
    return JsonResponse({'CarModels': models})

def analyze(request, text):
    t = text.lower()
    sentiment = 'positive' if any(w in t for w in ['fantastic','excellent','good','great','nice']) else 'negative'
    return JsonResponse({'sentiment': sentiment})
