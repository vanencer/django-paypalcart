from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django_paypalcart import PayPal
    
def checkout(request):
    if request.method == "POST":  
        baseurl = request.build_absolute_uri().replace('http://', '')
        baseurl = 'http://' + baseurl.split('/', 2)[0]
        
        paypal = PayPal.PayPal()
        response = paypal.SetExpressCheckout(
            cancelurl=baseurl + reverse('django_paypalcart.views.cancel'),
            returnurl=baseurl + reverse('django_paypalcart.views.confirm'),
            amt=request.POST['amount'],
            currencycode=request.POST['amount'])
        
        if response['ACK'] == 'Success':
            url = paypal.express_checkout_url + response['TOKEN']
            #url += '&useraction=commit' # Use to skip the confirm page
            return HttpResponseRedirect(url)
    
    return render_to_response('checkout.html')
    
    
def success(request):
    paypal = PayPal.PayPal()
    result = paypal.DoExpressCheckoutPayment(
        paymentaction='Sale',
        token=request.POST['token'],
        payerid=request.POST['payerid'],
        amt=request.POST['amount'])
    params = {'data':result}
    return render_to_response('success.html', params)

    
def cancel(request):
    return render_to_response('cancel.html')
    

def confirm(request):
    paypal = PayPal.PayPal()
    data = paypal.GetExpressCheckoutDetails(token=request.GET['token'])
    params = {'data':data, 'success_url':reverse('django_paypalcart.views.success')}
    return render_to_response('confirm.html', params)