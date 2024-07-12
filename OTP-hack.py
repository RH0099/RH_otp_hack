import imaplib
import email
import re
from email.header import decode_header

# জিমেইল IMAP সেটিংস
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# আপনার জিমেইল অ্যাকাউন্টের তথ্য
EMAIL = 'your_email@gmail.com'
PASSWORD = 'your_password'

def fetch_otp_from_gmail():
    try:
        # জিমেইল IMAP সার্ভারে লগইন
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        # ইনবক্স সিলেক্ট করুন
        mail.select('inbox')

        # OTP সাথে এসএমএস অনুসন্ধান করুন
        result, data = mail.search(None, '(UNSEEN SUBJECT "OTP")')

        otp_list = []

        for num in data[0].split():
            result, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # ইমেইলের বডি থেকে OTP বের করুন
            otp_pattern = r'\b\d{6}\b'  # OTP যদি 6 টি সংখ্যা হয়
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    otp = re.search(otp_pattern, body)
                    if otp:
                        otp_list.append(otp.group())
        
        return otp_list

    except Exception as e:
        print(f'OTP পেতে ত্রুটি: {str(e)}')
        return []

# উদাহরণ ব্যবহার
if __name__ == "__main__":
    otps = fetch_otp_from_gmail()
    if otps:
        print(f'OTP পাওয়া গেছে: {otps}')
    else:
        print('আপনার জিমেইল ইনবক্সে OTP পাওয়া যায়নি।')
