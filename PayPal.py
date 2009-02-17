import urllib, md5, datetime
from cgi import parse_qs
from django.core.urlresolvers import reverse
from django_paypalcart import default_settings as settings

class PayPal: 
    base_nvps = {}
    express_checkout_url = ''
    interface_url = ''

    def __init__(self):
        self.base_nvps = {
            'USER':       settings.PAYPALCART_API_USER,
            'PWD':        settings.PAYPALCART_API_PASSWORD,
            'SIGNATURE':  settings.PAYPALCART_API_SIGNATURE,
            'VERSION':    '53.0',
            }
        
        map = {'live':'', 'sandbox':'.sandbox', 'sandbox-beta':'.sandbox-beta'}
        self.express_checkout_url = \
            'https://www%s.paypal.com/webscr&cmd=_express-checkout&token=' % \
            map[settings.PAYPALCART_ENVIRONMENT]
            
        self.interface_url = 'https://api-3t%s.paypal.com/nvp' % \
            map[settings.PAYPALCART_ENVIRONMENT]
        
    def __request(self, params):
        """Perform the NVP request and return the response"""
        # Ready the parameters to be sent
        nvps = self.base_nvps
        nvps.update(params)
        nvps = dict((k.upper(), v) for k, v in nvps.items())

        # Query the NVP API
        response = urllib.urlopen(self.interface_url, urllib.urlencode(nvps)).read()
        
        # Format the response
        response = parse_qs(response)
        response = dict((k, v[0]) for k, v in response.items())
        return response
            
            
    ### Authorization and Capture API
    def DoCapture(self):
        """Capture an authorized payment"""
        [params[k] for k in ['method', 'authorizationid', 'amt', 'completetype']]
        params['method'] = 'DoCapture' 
        return self.__request(params)
        
    def DoAuthorization(self):
        """Authorize a payment"""
        [params[k] for k in ['method', 'transactionid', 'amt']]
        params['method'] = 'DoAuthorization' 
        return self.__request(params)
        
    def DoReauthorization(self):
        """Reauthorize a payment"""
        [params[k] for k in ['method', 'authorizationid', 'amt']]
        params['method'] = 'DoReauthorization' 
        return self.__request(params)
        
    def DoVoid(self):
        """Void an order or an authorization"""
        [params[k] for k in ['method', 'authorizationid']]
        params['method'] = 'DoVoid' 
        return self.__request(params)
    
    
    ### DoDirectPayment API
    def DoDirectPayment(self):
        """Process a credit card payment"""
        [params[k] for k in ['method', 'creditcardtype', 'acct']]
        params['method'] = 'DoDirectPayment' 
        return self.__request(params)
    
    ### Express Checkout API
    def SetExpressCheckout(self, params):
        """Initiates an Express Checkout transaction
        
        Optionally, the SetExpressCheckout API operation can set up billing agreements for 
        reference transactions and recurring payments.
        """
        [params[k] for k in ['returnurl', 'cancelurl', 'amt']]
        params['method'] = 'SetExpressCheckout' 
        return self.__request(params)
    
    
    def GetExpressCheckoutDetails(self, params):
        """Obtain information about an Express Checkout transaction"""
        [params[k] for k in ['token']]
        params['method'] = 'GetExpressCheckoutDetails' 
        return self.__request(params)
    
    
    def DoExpressCheckoutPayment(self, params):
        """Completes an Express Checkout transaction
        
        If you set up a billing agreement in your SetExpressCheckout API call, the billing 
        agreement is created when you call the DoExpressCheckoutPayment API operation.
        """
        [params[k] for k in ['token', 'paymentaction', 'payerid', 'amt']]
        params['method'] = 'DoExpressCheckoutPayment' 
        return self.__request(params)
      
          
    ### GetTransactionDetails API
    def GetTransactionDetails(self):
        """Obtain information about a specific transaction"""
        [params[k] for k in ['transactionid']]
        params['method'] = 'GetTransactionDetails' 
        return self.__request(params)                
    
    ### MassPay API
    def MassPay(self):
        """Make a payment to one or more PayPal account holders"""
        [params[k] for k in ['method']]
        params['method'] = 'MassPay' 
        return self.__request(params)              
              
    ### RefundTransaction API
    def RefundTransaction(self):
        """Issue a refund to the PayPal account holder associated with a transaction"""
        [params[k] for k in ['transactionid', 'refundtype']]
        params['method'] = 'RefundTransaction' 
        return self.__request(params)    
    
    ### TransactionSearch API
    def TransactionSearch(self):
        """Search transaction history for transactions that meet the specified criteria"""
        [params[k] for k in ['method', 'startdate']]
        params['method'] = 'TransactionSearch' 
        return self.__request(params)

    ### Recurring Payments and Reference Transactions API
    def CreateRecurringPaymentsProfile(self, token, startdate, desc, period, freq, amt):
        """Create a recurring payments profile
        
        You must invoke the CreateRecurringPaymentsProfile API operation for each profile 
        you want to create. The API operation creates a profile and an associated billing agreement.
        """
        [params[k] for k in ['method']]
        params['method'] = 'CreateRecurringPaymentsProfile' 
        return self.__request(params)
                
    def GetRecurringPaymentsProfileDetails(self):
        """Obtain information about a recurring payments profile"""
        [params[k] for k in []]
        params['method'] = 'GetRecurringPaymentsProfileDetails' 
        return self.__request(params)
            
    def ManageRecurringPaymentsProfileStatus(self):
        """Cancel, suspend, or reactivate a recurring payments profile"""
        [params[k] for k in []]
        params['method'] = 'ManageRecurringPaymentsProfileStatus' 
        return self.__request(params)
                
    def BillOutstandingAmount(self):
        """Bill the buyer for the outstanding balance associated with a recurring payments profile"""
        [params[k] for k in []]
        params['method'] = 'BillOutstandingAmount' 
        return self.__request(params)
                
    def UpdateRecurringPaymentsProfile(self):
        """Update a recurring payments profile"""
        [params[k] for k in []]
        params['method'] = 'UpdateRecurringPaymentsProfile' 
        return self.__request(params)
                
    def SetCustomerBillingAgreement(self):
        """Initiates the creation of a billing agreement"""
        [params[k] for k in []]
        params['method'] = 'SetCustomerBillingAgreement' 
        return self.__request(params)
                
    def GetBillingAgreementCustomerDetails(self):
        """Obtain information about a billing agreement?s PayPal account holder"""
        [params[k] for k in []]
        params['method'] = 'GetBillingAgreementCustomerDetails' 
        return self.__request(params)
                
    def BAUpdate(self):
        """Update or delete a billing agreement"""
        [params[k] for k in []]
        params['method'] = 'BAUpdate' 
        return self.__request(params)
                
    def DoReferenceTransaction(self):
        """Process a payment from a buyer?s account, which is identified by a previous transaction"""
        [params[k] for k in []]
        params['method'] = 'DoReferenceTransaction' 
        return self.__request(params)
                
        
    ### DoNonReferencedCredit API
    def DoNonReferencedCredit(self):
        """Issue a credit to a card not referenced by the original transaction"""
        [params[k] for k in []]
        params['method'] = 'DoNonReferencedCredit' 
        return self.__request(params)
            
            
    ### ManagePendingTransactionStatus API
    def ManagePendingTransactionStatus(self):
        """Accept or deny a pending transaction held by Fraud Management Filters"""
        [params[k] for k in []]
        params['method'] = 'ManagePendingTransactionStatus' 
        return self.__request(params)
            
    
    ### GetBalance API
    def GetBalance(self):
        """Obtain the available balance for a PayPal account"""
        [params[k] for k in []]
        params['method'] = 'GetBalance' 
        return self.__request(params)
            
    
    ### AddressVerify API
    def AddressVerify(self):
        """Confirms whether a postal address and postal code match those of the specified PayPal account holder"""
        [params[k] for k in ['method', 'email', 'street', 'zip']]
        params['method'] = 'AddressVerify' 
        return self.__request(params)
        