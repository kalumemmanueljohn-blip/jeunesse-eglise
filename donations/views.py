from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Donation

def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        phone_number = request.POST.get('phone_number')
        anonymous = request.POST.get('anonymous') == 'on'
        
        donation = Donation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            amount=amount,
            payment_method=payment_method,
            phone_number=phone_number,
            anonymous=anonymous,
        )
        messages.success(request, "Merci pour votre don ! Un message de confirmation vous sera envoyé.")
        return redirect('home')
    
    return render(request, 'donations/donate.html')