# coding: utf-8
import json
from flask import Flask, request
import coinapi_cl_ea as external_adapter
app = Flask(__name__)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/coinapi-cl-ea/', methods=['POST'])
def call_adapter():
    test_data = request.get_json()
    result = external_adapter.handler(test_data)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)


