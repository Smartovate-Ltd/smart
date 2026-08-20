import hashlib
import hmac


def verify_signature(payload_body: bytes, signature_header: str, secret: str) -> bool:
    if not signature_header:
        return False

    mac = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256,
    )

    expected_signature = f"sha256={mac.hexdigest()}"

    retur hmac.compare_digest(expected_signature, signature_header)
cc
