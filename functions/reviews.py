import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(dict):
    secret={
        "COUCH_URL": "Your URL",
        "IAM_API_KEY": "Your API_KEY",
        "COUCH_USERNAME": "Your USERNAME"
    }
    
    client = Cloudant.iam(
        account_name=secret["COUCH_USERNAME"],
        api_key=secret["IAM_API_KEY"],
        connect=True,
    )
    
    reviews_db = client["reviews"]
    
    try:
        selector = {'dealership': {'$eq': int(dict['id'])}}
        review_result = reviews_db.get_query_result(selector,raw_result=True)
        result = {
            'headers': {'Content-Type':'application/json'},
            'body': {'data': review_result}
        }
        return result
    
    except:
        return {
            'statusCode': '404',
            'message': 'dealerId does not exist'     
        }