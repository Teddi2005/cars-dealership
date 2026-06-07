from django.urls import path
from . import views

urlpatterns = [
    path('djangoapp/', views.home, name='home'),
    path('djangoapp/login', views.login_user, name='login'),
    path('djangoapp/logout', views.logout_user, name='logout'),
    path('djangoapp/register', views.register_user, name='register'),
    path('djangoapp/get_dealers', views.get_dealers, name='get_dealers'),
    path('djangoapp/get_dealers/<str:state>', views.get_dealers_by_state, name='get_dealers_by_state'),
    path('djangoapp/dealer/<int:dealer_id>', views.dealer_detail, name='dealer_detail'),
    path('djangoapp/review/<int:dealer_id>', views.review_dealer, name='review_dealer'),
    path('djangoapp/get_cars', views.get_cars, name='get_cars'),
    # Microservice-compatible endpoints on Django too
    path('fetchDealers', views.fetch_dealers, name='fetch_dealers'),
    path('fetchDealers/<str:state>', views.fetch_dealers_state, name='fetch_dealers_state'),
    path('fetchDealer/<int:dealer_id>', views.fetch_dealer, name='fetch_dealer'),
    path('fetchReviews/dealer/<int:dealer_id>', views.fetch_reviews, name='fetch_reviews'),
    path('analyze/<path:text>', views.analyze, name='analyze'),
]
