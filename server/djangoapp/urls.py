from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="root"),
    path("djangoapp/", views.home, name="home"),

    path("djangoapp/login", views.login_user, name="login"),
    path("djangoapp/logout", views.logout_user, name="logout"),
    path("djangoapp/register", views.register_user, name="register"),

    path("djangoapp/get_dealers", views.get_dealers, name="get_dealers"),
    path("djangoapp/get_dealers/<str:state>", views.get_dealers_by_state, name="get_dealers_by_state"),
    path("djangoapp/dealer/<int:dealer_id>", views.dealer_detail, name="dealer_detail"),
    path("djangoapp/review/<int:dealer_id>", views.review_dealer, name="review_dealer"),
    path("djangoapp/get_cars", views.get_cars, name="get_cars"),
    path("djangoapp/add_review", views.add_review, name="add_review"),

    # Node-compatible endpoints, served directly by Django.
    path("fetchDealers", views.fetch_dealers, name="fetch_dealers"),
    path("fetchDealers/<str:state>", views.fetch_dealers, name="fetch_dealers_state"),
    path("fetchDealer/<int:dealer_id>", views.fetch_dealer, name="fetch_dealer"),
    path("fetchReviews", views.fetch_all_reviews, name="fetch_all_reviews"),
    path("fetchReviews/dealer/<int:dealer_id>", views.fetch_reviews, name="fetch_reviews"),

    # Flask sentiment-compatible endpoint, served directly by Django.
    path("analyze/<path:text>", views.analyze, name="analyze"),
]
