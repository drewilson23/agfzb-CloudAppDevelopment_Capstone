import sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(dict):
    secret = {
         "COUCH_URL": "Your URL",
        "IAM_API_KEY": "Your API_KEY",
        "COUCH_USERNAME": "Your USERNAME"
    };
    
    client = Cloudant.iam(
        account_name=secret["COUCH_USERNAME"],
        api_key=secret["IAM_API_KEY"],
        connect=True,
        )
    
    reviews_db = client["reviews"]
    
    new_doc = reviews_db.create_document(dict)
    
    if new_doc.exists():
        result = {
            'headers' : {'Content-Type':'application/json'},
            'body': {'message':"Data Inserted"}
        }
        return result
    else:
        return {
            'statusCode': 500, 
            'message': 'Something went wrong'
        }