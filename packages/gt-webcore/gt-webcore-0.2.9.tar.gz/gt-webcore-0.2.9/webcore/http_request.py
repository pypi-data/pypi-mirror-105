# coding:utf-8
import json

import requests
from dotdict import DotDict
from flask import request

from webcore import constant, exception

def post(url, headers={}, data=None, json=None, send_token=True):
    send_token and _set_auth_header(headers)
    response = requests.post(
        url, 
        headers=headers, 
        json=json,
        data=data,
        verify=False)
    return _get_response_data(response)

def get(url, headers={}, params=None, send_token=True):
    send_token and _set_auth_header(headers)
    response = requests.get(
        url, 
        headers=headers, 
        params=params,
        verify=False)

    return _get_response_data(response)

def put(url, headers={}, data=None, send_token=True):
    send_token and _set_auth_header(headers)
    response = requests.put(
        url, 
        headers=headers,
        data=data,
        verify=False)
    return _get_response_data(response)

def delete(url, headers={}, params=None, send_token=True):
    send_token and _set_auth_header(headers)
    response = requests.delete(
        url, 
        headers=headers, 
        params=params, 
        verify=False)
    return _get_response_data(response)
    
def _set_auth_header(headers):
    if constant.AUTH_HEADER in headers:
        return

    token = request.headers.get(constant.AUTH_HEADER)
    headers[constant.AUTH_HEADER] = token

def _get_response_data(response):
    result = DotDict(response.json())

    if result.code != constant.Error.OK.value:
        raise exception.GtBaseError(result.code, result.msg, result.data)

    return result.data
