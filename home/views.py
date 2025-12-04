from django.shortcuts import render, redirect
from .models import FreeTip,VIP,AdminPayment
from paystackpy import Transaction 
from django.urls import reverse
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
import requests
import json
import uuid
from datetime import datetime

def tips_list(request):
    
    all_free_tips = FreeTip.objects.all().order_by('-date_posted')
    context = {
        'free_tips': all_free_tips
    }
    return render(request, 'list.html', context)

def vip(request):
    
    vip = VIP.objects.all().order_by('-date_posted')
    context = {
        'free_tips': vip
    }
    return render(request, 'vip.html', context)



paystack_transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)

def pay_for_admin_access(request: HttpRequest) -> HttpResponse:
    """
    Handles the payment form for admin access.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, "Email is required to proceed with payment.")
            return render(request, 'pay_for_admin.html')
        
        # Paystack requires amount in pesewas (100 pesewas = 1 Ghana Cedi)
        amount_in_pesewas = 50 * 100 
        
        # Generate a unique reference for the transaction
        reference = str(uuid.uuid4())

        # Paystack API endpoint for transaction initialization
        url = "https://api.paystack.co/transaction/initialize"
        
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "email": email,
            "amount": amount_in_pesewas,
            "reference": reference,
            "callback_url": request.build_absolute_uri('verify-admin-payment/'),
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            
            if data['status']:
                AdminPayment.objects.create(
                    email=email,
                    amount=50.00,
                    reference=reference,
                    is_verified=False
                )
                
                request.session['paystack_reference'] = reference
                
                return redirect(data['data']['authorization_url'])
            else:
                messages.error(request, data.get('message', 'Payment initialization failed.'))
                return render(request, 'pay_for_admin.html')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred while connecting to Paystack: {e}")
            return render(request, 'pay_for_admin.html')
            
    return render(request, 'payment.html')

def verify_admin_payment(request: HttpRequest) -> HttpResponse:
    """
    Verifies the payment and grants access to the admin page.
    """
    reference = request.GET.get('reference') or request.session.get('paystack_reference')
    
    if not reference:
        messages.error(request, "Payment verification failed. No reference provided.")
        return redirect('pay_for_admin')
    
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data['data']['status'] == 'success':
            try:
                payment = AdminPayment.objects.get(reference=reference)
                payment.is_verified = True
                payment.save()
                
                request.session['has_paid_for_admin'] = True
                
                del request.session['paystack_reference']
                
                messages.success(request, "Payment successful! You now have access.")
                return redirect('vip')
            except AdminPayment.DoesNotExist:
                messages.error(request, "Payment record not found. Please contact support.")
                return redirect('home')
        else:
            messages.error(request, f"Payment failed: {data['data']['status']}")
            return redirect('home')
    except requests.exceptions.RequestException as e:
        messages.error(request, f"An error occurred during verification: {e}")
        return redirect('home')    