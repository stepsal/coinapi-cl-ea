# coding: utf-8
import requests
import json
import urllib.parse
import os

ERRORS = dict({'400': 'Bad Request – There is something wrong with your request',
               '401': 'Unauthorized – Your API key is wrong',
               '403': 'Forbidden – Your API key doesnt’t have enough privileges to access this resource',
               '429': 'Too many requests – You have exceeded your API key rate limits',
               '550': 'No data – You requested specific single item that we don’t have at this moment',
               '404': 'Url not found'})

supported_endpoints = ['exchanges', 'assets', 'symbols',
                       'exchangerate', 'ohlcv', 'trades',
                       'quotes']

api_key = os.getenv("API_KEY")
api_url_prefix = "https://rest.coinapi.io/v1/"


def lambda_handler(event, context):
    result = handler(event)
    return result


def gcs_handler(request):
    cl_data = request.json
    result = handler(cl_data)
    return json.dumps(result)


def handler(cl_request_data):

    if 'data' not in cl_request_data:
        cl_request_data['data'] = {}
    if 'id' not in cl_request_data:
        cl_request_data['id'] = ""

    query_url = create_api_url(cl_request_data['data'])

    headers = {
        'X-CoinAPI-Key': api_key,
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate, gzip'}
    response = requests.get(query_url, headers=headers)
    error_string = None

    if response.status_code == 200:
        json_data = json.loads(response.text)
    else:
        if str(response.status_code) in ERRORS.keys():
            error_string = ERRORS[str(response.status_code)]
        else:
            error_string = "Unspecified Error"
        json_data = {}

    adapter_result = {'jobRunID': cl_request_data['id'],
                      'data': json_data,
                      'status': str(response.status_code)}

    if error_string is not None:
        adapter_result['error'] = error_string
    return adapter_result


def create_api_url(data):

    url = ""
    url += api_url_prefix

    if not data:
        return url

    data_dn = denormalise_parameters(data)

    if 'endpoint' not in data_dn:
        return url
    url += data_dn['endpoint']

    if data_dn['endpoint'] == 'exchangerate':
        if 'asset_id_base' in data_dn:
            url += "/" + data_dn['asset_id_base']
            if 'asset_id_quote' in data_dn:
                url += "/" + data_dn['asset_id_quote']

    if data_dn['endpoint'] in ['ohlcv', 'trades', 'quotes', 'orderbooks']:
        if 'symbol_id' in data_dn:
            url += "/" + data_dn['symbol_id']
        if 'path' in data_dn:
            url += "/" + data_dn['path']

    parameters = {k: v for k, v in data_dn.items() if k not in
                  ['endpoint', 'path', 'asset_id_base',
                   'asset_id_quote', 'symbol_id']}

    if len(parameters) > 0:
        encoded_params = urllib.parse.urlencode(parameters)
        url += '?' + encoded_params
    return url


def denormalise_parameters(input_dict):
    # Converts CamelCase key names to underscore_separated and returns a new dict
    result_dict = {}
    for k, v in input_dict.items():
        newk = ''.join(['_' + x.lower() if x.isupper() else x for x in k])
        result_dict[newk] = v
    return result_dict
