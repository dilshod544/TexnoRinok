import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_sms(phone, message):
    """
    Sends an SMS message using a provider (e.g., Eskiz.uz).
    In development, it just logs to the console/file.
    """
    # Clean phone number (must be 998901234567 format for Eskiz)
    clean_phone = ''.join(filter(str.isdigit, phone))
    if clean_phone.startswith('8'):
        clean_phone = '998' + clean_phone[1:]
    elif not clean_phone.startswith('998'):
        clean_phone = '998' + clean_phone
        
    logger.info(f"SMS to {clean_phone}: {message}")
    print(f"--- SMS SENT TO {clean_phone} ---")
    print(f"Message: {message}")
    print(f"--------------------------------")
    
    # Real API implementation example (uncomment and configure if you have Eskiz token)
    # ESKIZ_TOKEN = getattr(settings, 'ESKIZ_TOKEN', None)
    # if ESKIZ_TOKEN:
    #     try:
    #         res = requests.post(
    #             'https://notify.eskiz.uz/api/message/sms/send',
    #             headers={'Authorization': f'Bearer {ESKIZ_TOKEN}'},
    #             data={
    #                 'mobile_phone': clean_phone,
    #                 'message': message,
    #                 'from': '4546'
    #             }
    #         )
    #         return res.json()
    #     except Exception as e:
    #         logger.error(f"SMS sending failed: {e}")
    
    return True
