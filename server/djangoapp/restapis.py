from urllib import response
import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if "apikey" in kwargs:
            # Call get method of requests library with URL and parameters
            # Basic authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Something went wrong")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #print(type(dealer))
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerid):
    results = []
    # Call get_request with a URL and dealerId parameter
    json_result = get_request(url, dealerid=dealerid)
    if json_result:
        dealer =  json_result["body"]["rows"]
        dealer_doc = dealer["doc"]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
        results.append(dealer_obj)

    return results

def get_dealer_by_state(url, st):
    results = []
    # Call get_request with a URL and dealerId parameter
    json_result = get_request(url, st=st)
    if json_result:
        dealer =  json_result["body"]["rows"]
        dealer_doc = dealer["doc"]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
        results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    #print(json_result)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        #print(type(reviews))
        for review in reviews:
            try:
                review_obj = DealerReview(name=review["name"], id=review["id"], 
                dealership=review["dealership"], review=review["review"], purchase=review["purchase"],
                purchase_date=review["purchase_date"], car_make=review['car_make'],
                car_model=review['car_model'], car_year=review['car_year'], sentiment="none")
            except:
                review_obj = DealerReview(name = review["name"], id=review["id"],
                dealership=review["dealership"], review=review["review"], purchase=review["purchase"],
                purchase_date='none', car_make='none',
                car_model='none', car_year='none', sentiment="none")
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)      
            results.append(review_obj)
        #print(review_obj.sentiment)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = "lBZjo4Pf24fluTtlQB81Nf9MeRrIheFSueMk4SOm8RBW"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/5600ebfe-77b8-41f8-aadf-72e54c28dbb5"
    
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version ='2022-04-07',
        authenticator=authenticator
    )
    
    nlu.set_service_url(url)
    
    response = nlu.analyze(text=text,
                           features=Features(sentiment=SentimentOptions())).get_result()
    
    #print(json.dumps(response))
    sentiment_result = response["sentiment"]["document"]["label"]
    #print(sentiment_result)
    
    return sentiment_result