from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ["make"]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "year"]


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "city", "state", "zip"]
    search_fields = ["full_name", "city", "state"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "dealer", "name", "car_make", "car_model", "sentiment"]
    search_fields = ["name", "review", "sentiment"]
