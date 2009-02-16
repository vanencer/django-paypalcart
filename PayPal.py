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
        
    def __request(self, nvps):
        """Perform the NVP request and return the response"""
        params = self.base_nvps
        params.update(nvps)
        nvps = dict((k.upper(), v) for k, v in params.items())
        response = urllib.urlopen(self.interface_url, urllib.urlencode(nvps)).read()
        response = parse_qs(response)
        response = dict((k, v[0]) for k, v in response.items())
        return response
            
            
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
    def DoDirectPayment(self):
        """Process a credit card payment"""
        pass

    
    ### Express Checkout API
    def SetExpressCheckout(self, returnurl, cancelurl, amt, **kwargs):
        """Initiates an Express Checkout transaction
        
        Optionally, the SetExpressCheckout API operation can set up billing agreements for 
        reference transactions and recurring payments.
        """
        nvps = locals()
        nvps['method'] = 'SetExpressCheckout' 
        nvps.pop('self')
        return self.__request(nvps)
    
    
    def GetExpressCheckoutDetails(self, token, **kwargs):
        """Obtain information about an Express Checkout transaction"""
        nvps = locals()
        nvps['method'] = 'GetExpressCheckoutDetails' 
        nvps.pop('self')
        return self.__request(nvps)
    
    
    def DoExpressCheckoutPayment(self, token, paymentaction, payerid, amt, **kwargs):
        """Completes an Express Checkout transaction
        
        If you set up a billing agreement in your SetExpressCheckout API call, the billing 
        agreement is created when you call the DoExpressCheckoutPayment API operation.
        """
        nvps = locals()
        nvps['method'] = 'DoExpressCheckoutPayment' 
        nvps.pop('self')
        return self.__request(nvps)
      
          
    ### GetTransactionDetails API
    def GetTransactionDetails(self, transactionid, **kwargs):
        """Obtain information about a specific transaction"""
        nvps = locals()
        nvps['method'] = 'GetTransactionDetails' 
        nvps.pop('self')
        return self.__request(nvps)
                
    
    ### MassPay API
    def MassPay(self, **kwargs):
        """Make a payment to one or more PayPal account holders"""
        nvps = locals()
        nvps['method'] = 'MassPay' 
        nvps.pop('self')
        return self.__request(nvps)
              
              
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
        pass
        
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
        """Obtain information about a billing agreement?s PayPal account holder"""
        pass
        
    def BAUpdate(self):
        """Update or delete a billing agreement"""
        pass
        
    def DoReferenceTransaction(self):
        """Process a payment from a buyer?s account, which is identified by a previous transaction"""
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