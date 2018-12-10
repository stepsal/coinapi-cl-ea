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


## Sample Job Spec
Chainlink normalises all api parameters to camelcase ( eg assetIdBase will map to asset_id_base in the actual api query)
```
{
  "initiators": [
    {
      "type": "web",
      "params": {
      }
    }
  ],
  "tasks": [
    {
      "type": "coinapi-cl-ea-docker",
      "confirmations": 0,
      "params": {
        "endpoint": "exchangerate",
        "assetIdBase": "BTC",
        "assetIdQuote": "USD"
      }
    }
  ],
  "startAt": null,
  "endAt": null
```
## Sample Job Spec Result
```
{
  "id": "ceda5ccb18ee4effacacff3a451cfdd3",
  "jobId": "c0b6ebcf849b4ca7b7e14c3cc682bf27",
  "result": {
    "jobRunId": "ceda5ccb18ee4effacacff3a451cfdd3",
    "data": {
      "assetIdBase": "BTC",
      "assetIdQuote": "USD",
      "endpoint": "exchangerate",
      "rate": 3440.9833656611113,
      "time": "2018-12-10T21:48:03.9455953Z"
    },
    "status": "completed",
    "error": null
  },
  "status": "completed",
  "taskRuns": [
    {
      "id": "33ac1506792640579034f6d770b89221",
      "result": {
        "jobRunId": "ceda5ccb18ee4effacacff3a451cfdd3",
        "data": {
          "assetIdBase": "BTC",
          "assetIdQuote": "USD",
          "endpoint": "exchangerate",
          "rate": 3440.9833656611113,
          "time": "2018-12-10T21:48:03.9455953Z"
        },
        "status": "completed",
        "error": null
      },
      "status": "completed",
      "task": {
        "type": "coinapi-cl-ea-docker",
        "confirmations": 0,
        "params": {
          "assetIdBase": "BTC",
          "assetIdQuote": "USD",
          "endpoint": "exchangerate"
        }
      },
      "minimumConfirmations": 0
    }
  ],
  "createdAt": "2018-12-10T21:48:03.822052017Z",
  "completedAt": "2018-12-10T21:48:03.97080798Z",
  "creationHeight": null,
  "observedHeight": null,
  "overrides": {
    "jobRunId": "",
    "data": {
    },
    "status": "",
    "error": null
  },
  "initiator": {
    "type": "web",
    "params": {
```

## Other Examples
```test_data.json``` contains example payloads for all supported endpoints, paths and their parameters.

Full documentation for CoinAPI.io API can be found [here](https://docs.coinapi.io/)







