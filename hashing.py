import hashlib

def generate_hashes(input_value):
    # Genera los hashes MD5, SHA1, SHA224, SHA256, SHA384, y SHA512
    hashes = {}

    # MD5
    hash1 = hashlib.md5()
    hash1.update(input_value.encode())
    hashes['MD5'] = hash1.hexdigest()

    # SHA1
    hash2 = hashlib.sha1()
    hash2.update(input_value.encode())
    hashes['SHA1'] = hash2.hexdigest()

    # SHA224
    hash3 = hashlib.sha224()
    hash3.update(input_value.encode())
    hashes['SHA224'] = hash3.hexdigest()

    # SHA256
    hash4 = hashlib.sha256()
    hash4.update(input_value.encode())
    hashes['SHA256'] = hash4.hexdigest()

    # SHA384
    hash5 = hashlib.sha384()
    hash5.update(input_value.encode())
    hashes['SHA384'] = hash5.hexdigest()

    # SHA512
    hash6 = hashlib.sha512()
    hash6.update(input_value.encode())
    hashes['SHA512'] = hash6.hexdigest()

    return hashes