function main(params) { 
    
    secret={
   "COUCH_URL": "Your URL",
   "IAM_API_KEY": "Your API_KEY",
   "COUCH_USERNAME": ""
};

   console.log(params); 

   return new Promise(function (resolve, reject) { 
        const Cloudant = require('@cloudant/cloudant'); 
        const cloudant = Cloudant({ 
           url: secret.COUCH_URL, 
           plugins: {iamauth: {iamApiKey:secret.IAM_API_KEY}} 
        }); 

        const dealershipDb = cloudant.use('dealerships'); 

        if (params.state) { 
           // return dealership with this state 
            dealershipDb.find({
                "selector": {
                    "state": {
                        "$eq": params.state  
                    }
                }
            },  function (err, result) { 
                    if (err) { 
                        console.log("🚀 ~ file: index.js ~ line 20 ~ err", err) 
                        reject(err); 
                    } 

                    let code=200; 
                    // DB is empty
                    if (result.docs.length==0) { 
                        code= 404; 
                   } 

                   resolve({ 
                        statusCode: code, 
                        headers: { 'Content-Type': 'application/json' }, 
                        body: result 
                    }); 
                }); 

       } else if (params.id) { 
            id=parseInt(params.dealerId) 
            // return dealership with this state 
            dealershipDb.find({selector: {id:parseInt(params.id)}}, function (err, result) { 

                if (err) { 
                   console.log("🚀 ~ file: index.js ~ line 20 ~ err", err) 
                   reject(err); 
                } 

                let code=200; 

                if (result.docs.length==0) { 
                    code= 404; 
                } 

                resolve({ 
                   statusCode: code, 
                   headers: { 'Content-Type': 'application/json' }, 
                   body: result 
                }); 
            }); 

       } else { 
           // return all documents 
            dealershipDb.list({ include_docs: true }, function (err, result) { 

               if (err) { 
                    console.log("🚀 ~ file: index.js ~ line 35 ~ err", err) 
                    reject(err); 
               } 

            resolve({ 
                   statusCode: 200, 
                   headers: { 'Content-Type': 'application/json' }, 
                   body: result 
               }); 
           }); 
       } 
   }); 
} 

