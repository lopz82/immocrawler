from re import sub


def from_numeric(s: str) -> float:
    s = s.replace(".", "")
    if "," in s:
        integer, decimal = s.rsplit(",", 1)
        s = ".".join([integer, decimal])
    return float(sub(r'[^\d.]', '', s))


def from_text(s: str) -> str:
    return s.strip()
