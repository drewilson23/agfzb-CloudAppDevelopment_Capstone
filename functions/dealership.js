
function main(params) {

    secret = {
        "COUCH_URL": "Your URL",
        "IAM_API_KEY": "Your API_KEY",
        "COUCH_USERNAME": "Your USERNAME"
    };

    console.log(params);

    return new Promise(function (resolve, reject) {
        const Cloudant = require('@cloudant/cloudant');
        const cloudant = Cloudant({
            url: secret.COUCH_URL,
            plugins: {iamauth: {iamApiKey:secret.IAM_API_KEY}}
        });

        const dealershipDb = cloudant.use('dealerships');

        // return dealership with this state
        if(params.state) {
            dealershipDb.find({
                "selector": {
                    "state": {
                        "$eq" : params.state
                    }
                }
            }, function (err, result) {
                if(err) {
                    console.log(err)
                    reject(err);
                }

                let code = 200;
                // DB is empty
                if(result.docs.length==0){
                    code = 404;
                }

                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json'},
                    body: result
                });
            });
        // return dealership with this dealerId
        } else if (params.id) {
            id = parseInt(params.dealerId)
            dealershipDb.find({"selector": {id:parseInt(params.id)}}, function (err, result) {

                if(err) {
                    console.log(err)
                    reject(err);
                }

                let code = 200;

                if(result.docs.length==0) {
                    code = 404;
                }

                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json'},
                    body: result
                });
            });
        // return all dealerships
        } else {
            dealershipDb.list({include_docs: true}, function (err, result) {

                if(err) {
                    console.log(err)
                    reject(err);
                }

                resolve({
                    statusCode: 200,
                    headers: { 'Content-Type': 'application/json'},
                    body: result
                });
            });
        }

    });
}