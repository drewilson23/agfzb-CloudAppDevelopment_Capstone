from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return "Name: " + self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make  = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealerid = models.IntegerField(null=True)
    
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    COUP = 'coup'
    TRUCK = 'truck'
    TYPE_CHOICES = [(SEDAN, 'Sedan'),(SUV, 'Suv'),
        (COUP, 'Coup'),(WAGON, 'Wagon'),(TRUCK, 'Truck')]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField(null=True)
    def __str__(self):
        return "Name: " + self.name 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.city = city
        self.state = state
        self.st = st
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name
    
    def __str__(self):
        return "Dealer name: " + self.full_name
    
class DealerReview:
    def __init__(self, name, review, dealership, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    
    def __str__(self):
        return "Name: " + self.name + "," \
                "Review " + self.review 