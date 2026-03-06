import requests
import json
import hashlib
import hmac
from datetime import datetime
from django.conf import settings
from django.core.cache import cache

class EasyPayService:
    """
    Easypay Mobile Money API Integration
    Handles both MTN and Airtel payments
    Source: https://www.easypay.co.ug/kb/knowledge-base/open-mobile-money-api-uganda-mtn-airtel-africell-utl-m-sente/ [citation:10]
    """
    
    def __init__(self):
        # Get these from settings when you register
        self.base_url = "https://www.easypay.co.ug/api/"
        self.client_id = getattr(settings, 'EASYPAY_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'EASYPAY_CLIENT_SECRET', '')
        self.ipn_url = getattr(settings, 'EASYPAY_IPN_URL', 'https://cap.onrender.com/payments/webhook/')
    
    def _make_request(self, action, **kwargs):
        """
        Make API request to Easypay
        """
        payload = {
            'username': self.client_id,
            'password': self.client_secret,
            'action': action,
            **kwargs
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                'success': 0,
                'errormsg': f"Connection error: {str(e)}"
            }
    
    def deposit(self, phone_number, amount, reference, reason="Hostel booking payment"):
        """
        Request payment from customer (Incoming payment)
        
        Args:
            phone_number: Customer's phone number (format: 25677XXXXXXX)
            amount: Amount in UGX
            reference: Your unique order reference
            reason: Payment description
        
        Returns:
            {
                'success': 1,
                'data': {...}
            } or error
        """
        # Format phone number (remove any 0 prefix, add 256)
        if phone_number.startswith('0'):
            phone_number = '256' + phone_number[1:]
        
        payload = {
            'action': 'mmdeposit',
            'amount': amount,
            'currency': 'UGX',
            'phone': phone_number,
            'reference': reference,
            'reason': reason
        }
        
        return self._make_request(**payload)
    
    def payout(self, phone_number, amount, reference):
        """
        Send money to customer (Outgoing payment)
        Used for refunds or payouts
        """
        if phone_number.startswith('0'):
            phone_number = '256' + phone_number[1:]
        
        payload = {
            'action': 'mmpayout',
            'amount': amount,
            'currency': 'UGX',
            'phone': phone_number,
            'reference': reference
        }
        
        return self._make_request(**payload)
    
    def check_status(self, reference):
        """
        Check transaction status
        """
        payload = {
            'action': 'mmstatus',
            'reference': reference
        }
        
        return self._make_request(**payload)
    
    def check_balance(self):
        """
        Check your Easypay account balance
        """
        payload = {
            'action': 'checkbalance'
        }
        
        return self._make_request(**payload)
    
    @staticmethod
    def calculate_charges(amount):
        """
        Calculate mobile money charges based on amount
        Charges table from Easypay [citation:10]
        """
        if amount <= 2500:
            return 400
        elif amount <= 5000:
            return 440
        elif amount <= 15000:
            return 600
        elif amount <= 30000:
            return 800
        elif amount <= 45000:
            return 1000
        elif amount <= 60000:
            return 1300
        elif amount <= 125000:
            return 1500
        elif amount <= 250000:
            return 2000
        elif amount <= 500000:
            return 5000
        elif amount <= 1000000:
            return 7000
        elif amount <= 2000000:
            return 9000
        else:
            return 10000


# SMS Service via Easypay
def send_sms_via_easypay(phone_number, message):
    """
    Send SMS using Easypay (if they offer this service)
    Note: Check with Easypay if SMS is available
    """
    # This would be implemented if Easypay provides SMS service
    # For now, we'll use a print statement for development
    print(f"SMS to {phone_number}: {message}")
    return True