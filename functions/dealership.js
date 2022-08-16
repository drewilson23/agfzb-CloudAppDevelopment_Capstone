function main(params) {
    secret={
        "COUCH_URL": "",
        "IAM_API_KEY": "",
        "COUCH_USERNAME": ""
     };
     console.log(params);

     return new Promise(function (resolve, reject){
        const { CloudantV1 } = require('@ibm-cloud/cloudant');
        const { IamAuthenticator } = require('ibm-cloud-sdk-core');
        const authenticator = new IamAuthenticator({
            apikey: secret.IAM_API_KEY
            });
        const cloudant = new CloudantV1({ 
           authenticator: authenticator
     });

     cloudant.setServiceUrl(secret.COUCH_URL);

     if (params.state) {
        // return dealerships with this state
        cloudant.postFind({
            db:'dealerships', 
            selector:{st:params.state}    
        })
        .then((result)=>{
            let code = 200;
            if(result.result.docs.length == 0){
                code = 404;
            }
            resolve({
                statusCode: code,
                headers: {'Content-Type': 'application/json'},
                body: result.result.docs
            });
        }).catch((err)=>{
            reject(err);
            })
     } else if (params.id) {
        id = parseInt(params.dealerId)
        // return dealerships with this id
        cloudant.postFind({
            db: 'dealerships',
            selector:{id: parseInt(params.id)}
        })
        .then((result)=>{
            let code = 200;
            if(result.result.docs.length == 0){
                code = 404;
            }
            resolve({
                statusCode: code,
                headers: {'Content-Type': 'application/json'},
                body: result
            });
        }).catch((err)=>{
            reject(err);
        })
     } else {
        // return all documents
        cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true
        })
        .then((result)=>{
            resolve({
                statusCode: 200,
                headers: {'Content-Type': 'application/json'},
                body: result
            });
        });
     }
    });
}