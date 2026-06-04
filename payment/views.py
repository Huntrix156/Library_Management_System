# import base64
# import json
# from datetime import datetime
#
# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
#
# from library.settings import SHORTCODE, PASSKEY, CALLBACK_URL
# from .models import Payment
# from .mpesa import  get_access_token
#
#
# # Create your views here.
# def stk_push(
#     phone_number,
#     amount
# ):
#
#     access_token = get_access_token()
#
#     timestamp = datetime.now().strftime(
#         "%Y%m%d%H%M%S"
#     )
#
#     password = base64.b64encode(
#         f"{settings.SHORTCODE}{settings.PASSKEY}{timestamp}".encode()
#     ).decode()
#
#     payload = {
#         "BusinessShortCode": settings.SHORTCODE,
#         "Password": password,
#         "Timestamp": timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": amount,
#         "PartyA": phone_number,
#         "PartyB": settings.SHORTCODE,
#         "PhoneNumber": phone_number,
#         "CallBackURL": settings.CALLBACK_URL,
#         "AccountReference": "DenisLibrary",
#         "TransactionDesc": "Library Fine Payment"
#     }
#
#     headers = {
#         "Authorization":
#         f"Bearer {access_token}"
#     }
#
#     response = requests.post(
#         "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
#         # "STK_PUSH_ENDPOINT_FROM_SAFARICOM",
#         json=payload,
#         headers=headers
#     )
#
#     return response.json()
#
#
#
# # @login_required
# def make_payment(request):
#
#     if request.method == "POST":
#
#         amount = request.POST['amount']
#         phone = request.POST['phone']
#
#         response = stk_push(
#             phone,
#             amount
#         )
#
#         Payment.objects.create(
#             user=request.user,
#             phone_number=phone,
#             amount=amount,
#             merchant_request_id=response.get(
#                 'MerchantRequestID'
#             ),
#             checkout_request_id=response.get(
#                 'CheckoutRequestID'
#             )
#         )
#
#         return render(
#             request,
#             "payment_sent.html"
#         )
#
#     return render(
#         request,
#         # "payment_form.html"
#         "payment.html"
#     )
#
#
#
#
#
# @csrf_exempt
# def mpesa_callback(request):
#     try:
#         data = json.loads(request.body)
#     except json.JSONDecodeError:
#         return JsonResponse({"ResultCode": 1, "ResultDesc": "Bad request"}, status=400)
#
#     return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
#


import base64
import json
from datetime import datetime

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Payment
from .mpesa import get_access_token


def stk_push(phone_number, amount):
    access_token = get_access_token()
    timestamp    = datetime.now().strftime("%Y%m%d%H%M%S")
    password     = base64.b64encode(
        f"{settings.SHORTCODE}{settings.PASSKEY}{timestamp}".encode()
    ).decode()

    payload = {
        "BusinessShortCode": settings.SHORTCODE,
        "Password":          password,
        "Timestamp":         timestamp,
        "TransactionType":   "CustomerPayBillOnline",
        "Amount":            amount,
        "PartyA":            phone_number,
        "PartyB":            settings.SHORTCODE,
        "PhoneNumber":       phone_number,
        "CallBackURL":       settings.CALLBACK_URL,
        "AccountReference":  "DenisLibrary",
        "TransactionDesc":   "Library Fine Payment",
    }

    headers  = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload, headers=headers
    )
    return response.json()


@login_required
def make_payment(request):
    if request.method == "POST":
        amount = request.POST['amount']
        phone  = request.POST['phone']
        response = stk_push(phone, amount)
        Payment.objects.create(
            user=request.user,
            phone_number=phone,
            amount=amount,
            merchant_request_id=response.get('MerchantRequestID'),
            checkout_request_id=response.get('CheckoutRequestID'),
        )
        return render(request, "payment_sent.html")
    return render(request, "payment.html")


@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Bad request"}, status=400)
    # TODO: update Payment status from callback data
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})