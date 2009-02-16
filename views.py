from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django_paypalcart import PayPal
    
def checkout(request):
    if request.method == "POST":  
        paypal = PayPal.PayPal()
        token = paypal.SetExpressCheckout(request.POST['amount'], 'django_paypalcart.views.confirm', 'django_paypalcart.views.cancel')        
        paypal_url = paypal.URL_CHECKOUT + token
        #paypal_url += '&useraction=commit'
        return HttpResponseRedirect(paypal_url)
    return render_to_response('cart/checkout.html')
    
    
def success(request):
    paypal = PayPal.PayPal()
    result = paypal.DoExpressCheckoutPayment(request.POST['token'], request.POST['payerid'], request.POST['amount'])
    params = {'data':result}
    return render_to_response('cart/success.html', params)

    
def cancel(request):
    return render_to_response('cart/cancel.html')
    

def confirm(request):
    paypal = PayPal.PayPal()
    data = paypal.GetExpressCheckoutDetails(request.GET['token'])
    params = {'data':data, 'success_url':reverse('django_paypalcart.views.success')}
    return render_to_response('cart/confirm.html', params)