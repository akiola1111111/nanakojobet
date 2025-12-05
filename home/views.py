from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import FreeTip, VIP, AdminPayment
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
import requests
import json
import uuid
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

# DECORATOR TO CHECK IF USER HAS PAID FOR VIP ACCESS
def vip_access_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('has_paid_for_admin'):
            messages.warning(request, "Please pay for VIP access to view VIP tips.")
            return redirect('payment')
        return view_func(request, *args, **kwargs)
    return wrapper

# HOME PAGE - FREE TIPS FOR EVERYONE
def tips_list(request):
    # Get all tips ordered by date
    all_free_tips = FreeTip.objects.all().order_by('-date_posted')

    # Get today's date
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Filter tips by date
    today_tips = FreeTip.objects.filter(date_posted__date=today).order_by('-date_posted')
    yesterday_tips = FreeTip.objects.filter(date_posted__date=yesterday).order_by('-date_posted')
    tomorrow_tips = FreeTip.objects.filter(date_posted__date=tomorrow).order_by('-date_posted')

    context = {
        'free_tips': all_free_tips,
        'today_tips': today_tips,
        'yesterday_tips': yesterday_tips,
        'tomorrow_tips': tomorrow_tips,
        'current_date': today
    }
    return render(request, 'list.html', context)

# VIP PAGE - PROTECTED CONTENT
@vip_access_required
def vip(request):
    # Get all VIP tips
    all_vip_tips = VIP.objects.all().order_by('-date_posted')

    # Get today's date
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Filter VIP tips by date
    today_vip = VIP.objects.filter(date_posted__date=today).order_by('-date_posted')
    yesterday_vip = VIP.objects.filter(date_posted__date=yesterday).order_by('-date_posted')
    tomorrow_vip = VIP.objects.filter(date_posted__date=tomorrow).order_by('-date_posted')

    context = {
        'free_tips': all_vip_tips,
        'today_tips': today_vip,
        'yesterday_tips': yesterday_vip,
        'tomorrow_tips': tomorrow_vip,
        'current_date': today
    }
    return render(request, 'vip.html', context)

# PAYMENT PAGE
def pay_for_admin_access(request):
    """
    Handles the payment form for VIP access.
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, "Email is required to proceed with payment.")
            return render(request, 'payment.html')

        # Paystack requires amount in pesewas (100 pesewas = 1 Ghana Cedi)
        amount_in_pesewas = 50 * 100

        # Generate a unique reference
        reference = str(uuid.uuid4())

        # Paystack API endpoint
        url = "https://api.paystack.co/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        # Build callback URL
        callback_url = request.build_absolute_uri(reverse('verify_payment'))
        
        payload = {
            "email": email,
            "amount": amount_in_pesewas,
            "reference": reference,
            "callback_url": callback_url,
            "metadata": {
                "custom_fields": [
                    {
                        "display_name": "Payment For",
                        "variable_name": "payment_for",
                        "value": "VIP Tips Access"
                    }
                ]
            }
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()

            if data['status']:
                # Save payment record
                AdminPayment.objects.create(
                    email=email,
                    amount=50.00,
                    reference=reference,
                    is_verified=False
                )

                # Store reference in session
                request.session['paystack_reference'] = reference
                request.session['payment_email'] = email

                # Redirect to Paystack payment page
                return redirect(data['data']['authorization_url'])
            else:
                messages.error(request, data.get('message', 'Payment initialization failed.'))
                return render(request, 'payment.html')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'payment.html')
    
    # GET request - show payment form
    return render(request, 'payment.html')

# PAYMENT VERIFICATION
def verify_admin_payment(request):
    """
    Verifies the payment and grants VIP access.
    """
    reference = request.GET.get('reference') or request.session.get('paystack_reference')
    
    if not reference:
        messages.error(request, "Payment verification failed. No reference provided.")
        return redirect('payment')

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data['status'] and data['data']['status'] == 'success':
            try:
                # Update payment record
                payment = AdminPayment.objects.get(reference=reference)
                payment.is_verified = True
                payment.save()

                # Grant VIP access
                request.session['has_paid_for_admin'] = True
                request.session['payment_email'] = payment.email
                
                # Clear temporary session data
                if 'paystack_reference' in request.session:
                    del request.session['paystack_reference']

                messages.success(request, "Payment successful! You now have VIP access.")
                return redirect('vip')
            except AdminPayment.DoesNotExist:
                messages.error(request, "Payment record not found. Please contact support.")
                return redirect('payment')
        else:
            messages.error(request, f"Payment failed or pending. Please try again.")
            return redirect('payment')
    except requests.exceptions.RequestException as e:
        messages.error(request, f"An error occurred during verification: {str(e)}")
        return redirect('payment')
