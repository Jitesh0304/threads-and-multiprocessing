from functools import lru_cache
from botocore.signers import CloudFrontSigner
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

KEY_PAIR_ID = "K4ZT76V2ZPY9Q"  # from CloudFront console
PRIVATE_KEY_PATH = r"C:\Users\jites\Desktop\AWS notes\private_key.pem"

# save file in cache
@lru_cache()
def _load_private_key(path: str = PRIVATE_KEY_PATH):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

# Load private key
def _rsa_signer(message: bytes) -> bytes:
    priv = _load_private_key()
    return priv.sign(message, padding.PKCS1v15(), hashes.SHA1())

def generate_signed_url(resource_url: str, expire_in: int):
    expire_at = datetime.now(timezone.utc) + timedelta(seconds=expire_in)
    cf_signer = CloudFrontSigner(KEY_PAIR_ID, _rsa_signer)
    signed_url = cf_signer.generate_presigned_url(resource_url, date_less_than=expire_at)
    return signed_url

url = generate_signed_url("https://d1lyab9qluv75r.cloudfront.net/folder1/Semantic_segmentation.mp4", 120)
print(url)


