import urllib, md5, datetime
from cgi import parse_qs
from django.core.urlresolvers import reverse
from django.conf import settings

class CartError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)

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
            
    ### Authorization and Capture API
    def DoCapture(self):
        """Capture an authorized payment"""
        pass
        
    def DoAuthorization(self):
        """Authorize a payment"""
        pass
        
    def DoReauthorization(self):
        """Reauthorize a payment"""
        pass
        
    def DoVoid(self):
        """Void an order or an authorization"""
        pass
    
    
    ### DoDirectPayment API
    def DoDirectPayment(self, amt, ipaddress, acct, expdate, cvv2, firstname, lastname, cctype, street, city, state, zipcode):
        """Process a credit card payment"""
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

    
    ### Express Checkout API
    def SetExpressCheckout(self, amount, return_url, cancel_url, **kwargs):
        """Initiates an Express Checkout transaction
        
        Optionally, the SetExpressCheckout API operation can set up billing agreements for 
        reference transactions and recurring payments.
        """
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
        """Obtain information about an Express Checkout transaction"""
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
        """Completes an Express Checkout transaction
        
        If you set up a billing agreement in your SetExpressCheckout API call, the billing 
        agreement is created when you call the DoExpressCheckoutPayment API operation.
        """
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
      
          
    ### GetTransactionDetails API
    def GetTransactionDetails(self, tx_id):
        """Obtain information about a specific transaction"""
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
                
    
    ### MassPay API
    def MassPay(self, email, amt, note, email_subject):
        """Make a payment to one or more PayPal account holders"""
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
              
              
    ### RefundTransaction API
    def RefundTransaction(self):
        """Issue a refund to the PayPal account holder associated with a transaction"""
        pass
    
    
    ### TransactionSearch API
    def TransactionSearch(self):
        """Search transaction history for transactions that meet the specified criteria"""
        pass


    ### Recurring Payments and Reference Transactions API
    def CreateRecurringPaymentsProfile(self, token, startdate, desc, period, freq, amt):
        """Create a recurring payments profile
        
        You must invoke the CreateRecurringPaymentsProfile API operation for each profile 
        you want to create. The API operation creates a profile and an associated billing agreement.
        """
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
        
    def GetRecurringPaymentsProfileDetails(self):
        """Obtain information about a recurring payments profile"""
        pass
    
    def ManageRecurringPaymentsProfileStatus(self):
        """Cancel, suspend, or reactivate a recurring payments profile"""
        pass
        
    def BillOutstandingAmount(self):
        """Bill the buyer for the outstanding balance associated with a recurring payments profile"""
        pass
        
    def UpdateRecurringPaymentsProfile(self):
        """Update a recurring payments profile"""
        pass
        
    def SetCustomerBillingAgreement(self):
        """Initiates the creation of a billing agreement"""
        pass
        
    def GetBillingAgreementCustomerDetails(self):
        """Obtain information about a billing agreement’s PayPal account holder"""
        pass
        
    def BAUpdate(self):
        """Update or delete a billing agreement"""
        pass
        
    def DoReferenceTransaction(self):
        """Process a payment from a buyer’s account, which is identified by a previous transaction"""
        pass
        
        
    ### DoNonReferencedCredit API
    def DoNonReferencedCredit(self):
        """Issue a credit to a card not referenced by the original transaction"""
        pass
    
            
    ### ManagePendingTransactionStatus API
    def ManagePendingTransactionStatus(self):
        """Accept or deny a pending transaction held by Fraud Management Filters"""
        pass
    
    
    ### GetBalance API
    def GetBalance(self):
        """Obtain the available balance for a PayPal account"""
        pass
    
    
    ### AddressVerify API
    def AddressVerify(self):
        """Confirms whether a postal address and postal code match those of the specified PayPal account holder"""
        pass