import hashlib
import platform

def get_hash(string: str) -> int:
    hash = hashlib.md5()
    hash.update(string.encode())
    return int(hash.hexdigest(), 16)

def get_hostname() -> str:
    return platform.node()