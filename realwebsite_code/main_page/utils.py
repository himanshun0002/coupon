import pywhatkit as kit
import datetime

def send_whatsapp_otp(phone_number, otp):
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute + 1  # Send 1 min later to ensure proper scheduling

    message = f"Your OTP for coupon redemption is: {otp}. Please enter this code to proceed."

    try:
        kit.sendwhatmsg(f"+{phone_number}", message, hours, minutes)
        return True
    except Exception as e:
        print(f"Error sending WhatsApp OTP: {e}")
        return False
    
import datetime
import pywhatkit as kit

def send_whatsapp_promo_code(phone_number, otp):
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute + 1  # Send 1 min later to ensure proper scheduling

    message = f"Your OTP for coupon redemption is: {otp}. Please enter this code to proceed."

    try:
        kit.sendwhatmsg(f"+{phone_number}", message, hours, minutes)
        print(f"[DEBUG] OTP message scheduled for +{phone_number} at {hours}:{minutes}")
        return True
    except Exception as e:
        print(f"Error sending WhatsApp OTP: {e}")
        return False
