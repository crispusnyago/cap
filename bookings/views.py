from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .services.easypay_service import EasyPayService
from .services.otp_service import OTPService
import uuid
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hostels.models import Hostel

@login_required
def create_booking(request, hostel_id):
    """Create a new booking"""
    hostel = get_object_or_404(Hostel, id=hostel_id)
    
    if request.method == 'POST':
        # Process booking (we'll add full logic later)
        messages.success(request, f'Booking request received for {hostel.name}')
        return redirect('hostels:list')
    
    return redirect('hostels:detail', pk=hostel_id)
@login_required
def initiate_payment(request, booking_id):
    """
    Step 1: Initiate payment with OTP verification
    """
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')  # 'mtn' or 'airtel'
        
        # Send OTP first
        success, message, otp = OTPService.send_otp(phone_number)
        
        if success:
            # Store payment details in session temporarily
            request.session['pending_payment'] = {
                'booking_id': booking.id,
                'phone_number': phone_number,
                'payment_method': payment_method,
                'amount': float(booking.amount_paid),
                'otp_verified': False
            }
            return redirect('bookings:verify_otp')
        else:
            messages.error(request, message)
            return redirect('bookings:payment', booking_id=booking.id)
    
    return render(request, 'bookings/initiate_payment.html', {'booking': booking})


@login_required
def verify_otp(request):
    """
    Step 2: Verify OTP before processing payment
    """
    pending = request.session.get('pending_payment')
    
    if not pending:
        messages.error(request, 'No pending payment found.')
        return redirect('bookings:my_bookings')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        phone_number = pending['phone_number']
        
        is_valid, message = OTPService.verify_otp(phone_number, entered_otp)
        
        if is_valid:
            # Mark as verified and proceed to payment
            pending['otp_verified'] = True
            request.session['pending_payment'] = pending
            return redirect('bookings:process_payment')
        else:
            messages.error(request, message)
    
    return render(request, 'bookings/verify_otp.html')


@login_required
def process_payment(request):
    """
    Step 3: Process actual payment after OTP verification
    """
    pending = request.session.get('pending_payment')
    
    if not pending or not pending.get('otp_verified'):
        messages.error(request, 'Payment not verified. Please start over.')
        return redirect('bookings:my_bookings')
    
    booking = get_object_or_404(Booking, id=pending['booking_id'])
    
    # Initialize Easypay service
    easypay = EasyPayService()
    
    # Generate unique reference
    reference = f"CAP-{booking.id}-{uuid.uuid4().hex[:8].upper()}"
    
    # Process payment
    result = easypay.deposit(
        phone_number=pending['phone_number'],
        amount=pending['amount'],
        reference=reference,
        reason=f"Hostel booking: {booking.hostel.name}"
    )
    
    if result.get('success') == 1:
        # Payment initiated successfully
        booking.payment_reference = reference
        booking.status = 'processing'
        booking.save()
        
        # Clear session
        del request.session['pending_payment']
        
        messages.success(request, 'Payment initiated. Please check your phone to complete the transaction.')
        return redirect('bookings:payment_status', booking_id=booking.id)
    else:
        messages.error(request, result.get('errormsg', 'Payment failed. Please try again.'))
        return redirect('bookings:payment', booking_id=booking.id)


@csrf_exempt
def payment_webhook(request):
    """
    Handle instant payment notifications from Easypay [citation:10]
    This URL should be set as your IPN URL in Easypay settings
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract payment details
            phone = data.get('phone')
            reference = data.get('reference')
            transaction_id = data.get('transactionId')
            amount = data.get('amount')
            
            # Find the booking
            try:
                booking = Booking.objects.get(payment_reference=reference)
                
                # Update booking status
                booking.status = 'confirmed'
                booking.transaction_id = transaction_id
                booking.payment_date = datetime.now()
                booking.save()
                
                # Create payment record
                payment = Payment.objects.create(
                    booking=booking,
                    amount=amount,
                    phone_number=phone,
                    network='mtn',  # You might need to detect this
                    transaction_id=transaction_id,
                    status='completed',
                    callback_data=data
                )
                
                # Send confirmation email
                send_booking_confirmation(booking)
                
                return JsonResponse({'status': 'success'})
                
            except Booking.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def payment_status(request, booking_id):
    """
    Check payment status
    """
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    
    # If using Easypay, you can check status via their API
    easypay = EasyPayService()
    result = easypay.check_status(booking.payment_reference)
    
    context = {
        'booking': booking,
        'status_result': result
    }
    return render(request, 'bookings/payment_status.html', context)