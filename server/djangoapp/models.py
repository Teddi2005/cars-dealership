from django.db import models


class Dealer(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=20)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField(default=2024)
    purchase = models.BooleanField(default=True)
    review = models.TextField()
    sentiment = models.CharField(max_length=30, default="positive")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.dealer.full_name}"


class CarMake(models.Model):
    make = models.CharField(max_length=100)

    def __str__(self):
        return self.make


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    model = models.CharField(max_length=100)
    year = models.IntegerField(default=2024)

    def __str__(self):
        return f"{self.make.make} {self.model}"
