import sys 
from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(dict): 
    secret = {
        "COUCH_URL": "https://62d823ce-50ed-4113-aecd-3e3dd99d3347-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "LiDJ3fVIxNsBaixdbsmQ1Jdar9iYgE7UnnNcOKTwFEMc",
        "COUCH_USERNAME": "62d823ce-50ed-4113-aecd-3e3dd99d3347-bluemix"
    }
    
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
            'statusCode': 404, 
            'message': 'Something went wrong'
        }
