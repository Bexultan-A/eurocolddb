import re
from typing import Optional

def normalize_phone_e164(v: Optional[str]) -> Optional[str]:
    if not v:
        return v
    digits = re.sub(r"\D", "", v)
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    if digits.startswith("7"):
        return f"+{digits}"
    return f"+{digits}" if digits and not v.startswith("+") else v
