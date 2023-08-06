# standard libs
import hashlib
import re

# local imports
from .constants import MOBILE_PATTERN


def is_mobile_number_valid(mobile_no):
    return bool(re.match(MOBILE_PATTERN, mobile_no))

def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()
