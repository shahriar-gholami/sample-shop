import requests
import json
from shop.models import Product


def send_domain_warn_msg(phone_number, owner_name):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
    "code": "lyp3pvrmj2sw81l",
    "sender": "+983000505",
    "recipient": phone_number,
    "variable": {
        "name": owner_name
    }
    })
    headers = {
    'apikey': 'q41yDW73vhtH5Xr63XYQ39DTo96yavuxGRiA9g4a79A=',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)



def send_gw_warn_msg(phone_number, owner_name):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
    "code": "fsjb9kghsqoilaf",
    "sender": "+983000505",
    "recipient": phone_number,
    "variable": {
        "name": owner_name
    }
    })
    headers = {
    'apikey': 'q41yDW73vhtH5Xr63XYQ39DTo96yavuxGRiA9g4a79A=',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def send_otp_code(phone_number, code):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
    "code": "6zxou8xsmhi8fot",
    "sender": "+983000505",
    "recipient": phone_number,
    "variable": {
        "verification-code": code

    }
    })
    headers = {
    'apikey': 'q41yDW73vhtH5Xr63XYQ39DTo96yavuxGRiA9g4a79A=',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def site_req_inform(phone_number, name):
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    payload = json.dumps({
    "code": "asvyx199bprr92n",
    "sender": "+983000505",
    "recipient": phone_number,
    "variable": {
        "name": name
    }
    })
    headers = {
    'apikey': 'q41yDW73vhtH5Xr63XYQ39DTo96yavuxGRiA9g4a79A=',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


    payload = json.dumps({
    "code": "jsnfbvmt5lmn7pz",
    "sender": "+983000505",
    "recipient": '09910412672',
    "variable": {
        "name": name
    }
    })
    headers = {
    'apikey': 'q41yDW73vhtH5Xr63XYQ39DTo96yavuxGRiA9g4a79A=',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def erase_stock_volume(product):
    product_varieties = product.get_varieties()
    for variety in product_varieties:
        variety.stock = 0
        variety.save()  

def update_slugs(modeladmin, request, queryset):
    for product in queryset:
        product.slug = product.name.replace(' ', '-')
        product.save()
    # نمایش پیام تایید برای کاربر
    modeladmin.message_user(request, "Slugs updated successfully!")










