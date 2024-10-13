import hashlib

def generate_hashes(input_value):
    # Diccionario para almacenar los hashes
    hashes = {}

    # MD5
    hash1 = hashlib.md5()
    hash1.update(input_value.encode())
    hashes['MD5'] = hash1.hexdigest()

    # SHA256
    hash4 = hashlib.sha256()
    hash4.update(input_value.encode())
    hashes['SHA256'] = hash4.hexdigest()

    # SHA3-256
    hash_sha3_256 = hashlib.sha3_256()
    hash_sha3_256.update(input_value.encode())
    hashes['SHA3-256'] = hash_sha3_256.hexdigest()

    return hashes