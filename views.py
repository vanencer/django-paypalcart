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
            response = paypal.SetExpressCheckout(
                cancelurl    = baseurl + reverse('django_paypalcart.views.cancel'),
                returnurl    = baseurl + reverse('django_paypalcart.views.confirm'),
                amt          = request.POST['amt'],
                currencycode = request.POST['currencycode'])
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
        response = paypal.DoExpressCheckoutPayment(
            paymentaction='Sale',
            token=request.POST['token'],
            payerid=request.POST['payerid'],
            amt=request.POST['amount'])
        assert response['ACK'] == 'Success'
    except IOError:
        return render_to_response('error.html', {'type':'IOError'})
    except KeyError, e:
        return render_to_response('error.html', {'type':'KeyError'})
    except AssertionError, e:
        return render_to_response('error.html', {'type':'ProcessingError', 'response':response})

    # Everything seems to have gone okay and the customer is charged
    # We might want to check PAYMENTSTATUS == Completed | Pending and decide what to do
    
    
    params = {'response':response}
    return render_to_response('success.html', params)

    
def cancel(request):
    return render_to_response('cancel.html')
    

def confirm(request):
    paypal = PayPal.PayPal()
    try:
        response = paypal.GetExpressCheckoutDetails(token=request.GET['token'])
        assert response['ACK'] == 'Success'
    except IOError:
        return render_to_response('error.html', {'type':'IOError'})
    except KeyError, e:
        return render_to_response('error.html', {'type':'KeyError'})
    except AssertionError, e:
        return render_to_response('error.html', {'type':'ProcessingError', 'response':response})

    params = {'response':response, 'success_url':reverse('django_paypalcart.views.success')}
    return render_to_response('confirm.html', params)