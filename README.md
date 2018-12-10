# CoinAPI.io Python 3.x External Adapter for Chainlink

**Adapter Formats**: Google Cloud Function, AWS Lambda and Docker

**Supported Endpoints**: exchanges, assets, symbols, exchangerate, ohlcv, trades, quotes

**Unsupported Endpoints**: subscriptions

**API Mapping**: A ```path``` parameter has been introduced to specify historical/current/latest/ for certain endpoints

## Cloud Installation:
Make the bash script executable

```chmod +x ./create_zip.bsh```

Create the adapter zip for your cloud provider ( gcs or aws )

```./create_zip.bsh aws```

Upload the created zip to your provider and set the appropriate handler ( gcs_handler or aws_handler ) to be triggered by a HTTP event.

Create an API_KEY environment variable and set it to your CoinAPI.io api key

## Docker Installation:
Build the image
```
docker build -t coinapi-cl-ea .
```
Run the container while passing in your API_KEY
```
docker run -e API_KEY=XXXXXXXX-XXXX-XXX-XXXX-XXXXXXXXXXX -p 5000:5000 coinapi-cl-ea
```
The adapter endpoint will be accessable from ```http://localhost/:5000/coinapi-cl-ea```

## Example
Chainlink Request JSON
```
{ "id": "278c97ffadb54a5bbb93cfec5f7b5503",
  "data": {"endpoint" : "exchangerate",
           "assetIdBase" : "BTC",
           "assetIdQuote" : "EUR"}}
```

Adapter Result:
```
{ "jobRunID": "278c97ffadb54a5bbb93cfec5f7b5503",
  "data": {"time": "2018-12-04T21:28:33.2112276Z",
           "assetIdBase": "BTC",
           "assetIdQuote": "EUR",
           "rate": 3425.7987980367275},
  "status": 200}
```
## Other Examples
```test_data.json``` contains example payloads for all supported endpoints, paths and their parameters.

Full documentation for CoinAPI.io API can be found [here](https://docs.coinapi.io/)







