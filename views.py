from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django_paypalcart import PayPal
    
def checkout(request):
    if request.method == "POST":  
        baseurl = request.build_absolute_uri().replace('http://', '')
        baseurl = 'http://' + baseurl.split('/', 2)[0]
        paypal = PayPal.PayPal()
        try:
            params = {
                'cancelurl':    baseurl + reverse('django_paypalcart.views.cancel'),
                'returnurl':    baseurl + reverse('django_paypalcart.views.confirm'),
                'amt':          request.POST['amt'],
                'currencycode': request.POST['currencycode']
                }
            response = paypal.SetExpressCheckout(params)
            assert response['ACK'] == 'Success'
            assert response['TOKEN']
        except IOError:
            return render_to_response('error.html', {'type':'IOError'})
        except KeyError, e:
            return render_to_response('error.html', {'type':'KeyError'})
        except AssertionError, e:
            return render_to_response('error.html', {'type':'ProcessingError', 'response':response})
        
        url = paypal.express_checkout_url + response['TOKEN']
        #url += '&useraction=commit' # Use to skip the confirm page
        return HttpResponseRedirect(url)
            
    return render_to_response('checkout.html')
    
    
def success(request):
    paypal = PayPal.PayPal()
    try:
        params = {
            'paymentaction': 'Sale',
            'token':         request.POST['token'],
            'payerid':       request.POST['payerid'],
            'amt':           request.POST['amount'],
            'currencycode':  request.POST['currencycode']
            }
        response = paypal.DoExpressCheckoutPayment(params)
        assert response['ACK'] == 'Success'
    except IOError:
        return render_to_response('error.html', {'type':'IOError'})
    except KeyError, e:
        return render_to_response('error.html', {'type':'KeyError'})
    except AssertionError, e:
        return render_to_response('error.html', {'type':'ProcessingError', 'response':response})

    # Everything seems to have gone okay and the customer is charged
    # Things to consider before sending digital goods:
    #   Check PAYMENTSTATUS. It might be "Completed" or "Pending"
    #   Check PAYMENTTYPE. It might be "instant" (you have the cash) or "echeque" (could bounce)    
    
    params = {'response':response}
    return render_to_response('success.html', params)

    
def cancel(request):
    return render_to_response('cancel.html')
    

def confirm(request):
    paypal = PayPal.PayPal()
    try:
        params = {'token': request.GET['token']}
        response = paypal.GetExpressCheckoutDetails(params)
        assert response['ACK'] == 'Success'
    except IOError:
        return render_to_response('error.html', {'type':'IOError'})
    except KeyError, e:
        return render_to_response('error.html', {'type':'KeyError'})
    except AssertionError, e:
        return render_to_response('error.html', {'type':'ProcessingError', 'response':response})

    params = {'response':response, 'success_url':reverse('django_paypalcart.views.success')}
    return render_to_response('confirm.html', params)