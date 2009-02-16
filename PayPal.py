# This aims to be a complete implementation of the Web Payments Pro API
# Based on original at: http://www.djangosnippets.org/snippets/1181/
# This code resides in the Public Domain - no restrictions are attached.

import urllib, md5, datetime
from cgi import parse_qs
from django.core.urlresolvers import reverse
from django.conf import settings

class PayPal:    
    URL_BASE      = 'http://127.0.0.1:8000'
    URL_CHECKOUT  = 'https://www.sandbox.paypal.com/webscr&cmd=_express-checkout&token='
    URL_NVP       = 'https://api-3t.sandbox.paypal.com/nvp'
    
    def __init__(self):
        signature_values = {
            'USER':      settings.PAYPALCART_API_USER,
            'PWD':       settings.PAYPALCART_API_PASSWORD,
            'SIGNATURE': settings.PAYPALCART_API_SIGNATURE,
            'VERSION':   '53.0',
            }
        self.signature = urllib.urlencode(signature_values) + "&"


    def SetExpressCheckout(self, amount, return_url, cancel_url, **kwargs):
        return_url = self.URL_BASE + reverse(return_url)
        cancel_url = self.URL_BASE + reverse(cancel_url)
        params = {
            'METHOD':        "SetExpressCheckout",
            'NOSHIPPING':    1,
            'PAYMENTACTION': 'Sale',
            'RETURNURL':     return_url,
            'CANCELURL':     cancel_url,
            'AMT':           amount,
        }
        params.update(kwargs)
        params_string = self.signature + urllib.urlencode(params)
        try:
            response = urllib.urlopen(self.URL_NVP, params_string).read()
            response_dict = parse_qs(response)
            assert response_dict['ACK'][0] == 'Success'
            response_token = response_dict['TOKEN'][0]
        except (AssertionError, IOError, KeyError):
            raise CartError(response_dict)
        return response_token
    
    
    def GetExpressCheckoutDetails(self, token, **kwargs):
        params = {
            'METHOD':    "GetExpressCheckoutDetails",
            'TOKEN' :    token,
        }
        params.update(kwargs)
        params_string = self.signature + urllib.urlencode(params)
        try:
            response = urllib.urlopen(self.URL_NVP, params_string).read()
            response_dict = parse_qs(response)
        except (IOError, KeyError):
            raise PayPalException({})
        return response_dict
    
    
    def DoExpressCheckoutPayment(self, token, payerid, amt):
        params = {
            'METHOD' : "DoExpressCheckoutPayment",
            'PAYMENTACTION' : 'Sale',
            'TOKEN' : token,
            'AMT' : amt,
            'PAYERID': payerid,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.URL_NVP, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])
        return response_tokens
        
        
    def GetTransactionDetails(self, tx_id):
        params = {
            'METHOD' : "GetTransactionDetails", 
            'TRANSACTIONID' : tx_id,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
                response_tokens[key] = urllib.unquote(response_tokens[key])
        return response_tokens
                
                
    def MassPay(self, email, amt, note, email_subject):
        unique_id = str(md5.new(str(datetime.datetime.now())).hexdigest())
        params = {
            'METHOD' : "MassPay",
            'RECEIVERTYPE' : "EmailAddress",
            'L_AMT0' : amt,
            'CURRENCYCODE' : 'USD',
            'L_EMAIL0' : email,
            'L_UNIQUE0' : unique_id,
            'L_NOTE0' : note,
            'EMAILSUBJECT': email_subject,
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
                response_tokens[key] = urllib.unquote(response_tokens[key])
        response_tokens['unique_id'] = unique_id
        return response_tokens
              
                
    def DoDirectPayment(self, amt, ipaddress, acct, expdate, cvv2, firstname, lastname, cctype, street, city, state, zipcode):
        params = {
            'METHOD' : "DoDirectPayment",
            'PAYMENTACTION' : 'Sale',
            'AMT' : amt,
            'IPADDRESS' : ipaddress,
            'ACCT': acct,
            'EXPDATE' : expdate,
            'CVV2' : cvv2,
            'FIRSTNAME' : firstname,
            'LASTNAME': lastname,
            'CREDITCARDTYPE': cctype,
            'STREET': street,
            'CITY': city,
            'STATE': state,
            'ZIP':zipcode,
            'COUNTRY' : 'United States',
            'COUNTRYCODE': 'US',
            'RETURNURL' : 'http://www.yoursite.com/returnurl', #edit this 
            'CANCELURL' : 'http://www.yoursite.com/cancelurl', #edit this 
            'L_DESC0' : "Desc: ",
            'L_NAME0' : "Name: ",
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])
        return response_tokens
    
    
    def CreateRecurringPaymentsProfile(self, token, startdate, desc, period, freq, amt):
        params = {
            'METHOD': 'CreateRecurringPaymentsProfile',
            'PROFILESTARTDATE': startdate,
            'DESC':desc,
            'BILLINGPERIOD':period,
            'BILLINGFREQUENCY':freq,
            'AMT':amt,
            'TOKEN':token,
            'CURRENCYCODE':'USD',
        }
        params_string = self.signature + urllib.urlencode(params)
        response = urllib.urlopen(self.API_ENDPOINT, params_string).read()
        response_dict = parse_qs(response)
        return response_dict
        
        
class CartError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)
