# bookings/services/otp_service.py
import random
import time
from typing import Dict, Tuple, Optional

class OTPService:
    """Service for handling OTP (One-Time Password) operations"""
    
    # In-memory storage for OTPs (in production, use Redis or database)
    _otp_storage: Dict[str, Dict] = {}
    
    @classmethod
    def generate_otp(cls, identifier: str, length: int = 6, expiry_seconds: int = 300) -> str:
        """
        Generate an OTP for a given identifier (phone number or email)
        
        Args:
            identifier: Phone number or email to associate with OTP
            length: Length of OTP (default 6)
            expiry_seconds: OTP expiry time in seconds (default 300 seconds / 5 minutes)
        
        Returns:
            Generated OTP code
        """
        # Generate random OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        
        # Store OTP with timestamp
        cls._otp_storage[identifier] = {
            'otp': otp,
            'timestamp': time.time(),
            'expiry': expiry_seconds,
            'attempts': 0
        }
        
        return otp
    
    @classmethod
    def verify_otp(cls, identifier: str, otp: str, max_attempts: int = 3) -> Tuple[bool, str]:
        """
        Verify an OTP for a given identifier
        
        Args:
            identifier: Phone number or email
            otp: OTP to verify
            max_attempts: Maximum number of verification attempts allowed
        
        Returns:
            Tuple of (is_valid, message)
        """
        # Check if OTP exists for identifier
        if identifier not in cls._otp_storage:
            return False, "OTP not found or expired"
        
        otp_data = cls._otp_storage[identifier]
        
        # Check attempts
        if otp_data['attempts'] >= max_attempts:
            # Clear OTP after max attempts
            del cls._otp_storage[identifier]
            return False, "Maximum attempts exceeded. Please request new OTP."
        
        # Increment attempts
        otp_data['attempts'] += 1
        
        # Check expiry
        current_time = time.time()
        if current_time - otp_data['timestamp'] > otp_data['expiry']:
            del cls._otp_storage[identifier]
            return False, "OTP has expired"
        
        # Verify OTP
        if otp_data['otp'] == otp:
            # Clear OTP after successful verification
            del cls._otp_storage[identifier]
            return True, "OTP verified successfully"
        else:
            return False, f"Invalid OTP. {max_attempts - otp_data['attempts']} attempts remaining"
    
    @classmethod
    def send_otp_sms(cls, phone_number: str, otp: str) -> bool:
        """
        Send OTP via SMS (implement with your SMS provider)
        
        This is a placeholder - integrate with services like Twilio, Africa's Talking, etc.
        """
        # TODO: Implement SMS sending logic
        # Example with Africa's Talking:
        # import requests
        # response = requests.post(
        #     'https://api.africastalking.com/version1/messaging',
        #     headers={'apiKey': 'YOUR_API_KEY'},
        #     data={'username': 'YOUR_USERNAME', 'to': phone_number, 'message': f'Your OTP is: {otp}'}
        # )
        # return response.status_code == 201
        
        print(f"SMS OTP {otp} to {phone_number}")  # For development
        return True
    
    @classmethod
    def send_otp_email(cls, email: str, otp: str) -> bool:
        """
        Send OTP via email (implement with your email service)
        
        This is a placeholder - integrate with services like SendGrid, Mailgun, etc.
        """
        # TODO: Implement email sending logic
        print(f"Email OTP {otp} to {email}")  # For development
        return True