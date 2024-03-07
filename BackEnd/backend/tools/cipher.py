import rsa

PATH_PUBKEY = "/olok_service/tools/keys/pubkey.pem"
PATH_PRIVKEY = "/olok_service/tools/keys/privkey.pem"

def generate_keys():
    (pubKey,privKey) = rsa.newkeys(1024)
    with open(PATH_PUBKEY, 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))

    with open(PATH_PRIVKEY, 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))

def load_keys():
    with open(PATH_PUBKEY, 'rb') as f:
        pubKey = rsa.PublicKey.load_pkcs1(f.read())

    with open(PATH_PRIVKEY, 'rb') as f:
        privKey = rsa.PrivateKey.load_pkcs1(f.read())

    return pubKey, privKey

def encrypt(msg):
    pubKey, privKey = load_keys()
    cipher_msg = rsa.encrypt(msg.encode('ascii'), pubKey)
    return (cipher_msg, sign_sha1(msg, privKey))

def decrypt(ciphertext, signature):
    pubKey, privKey = load_keys()
    try:
        decipher_msg = rsa.decrypt(ciphertext, privKey).decode('ascii')
        return (decipher_msg, verify_sha1(decipher_msg, signature, pubKey))
    except:
        return False

def sign_sha1(msg,key):
    return rsa.sign(msg.encode('ascii'), key, 'SHA-1')

def verify_sha1(msg, signature, key):
    try:
        return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False

"""
message = input('Enter a message:')
(ciphertext, signature) = encrypt(message)

(plaintext, signature) = decrypt(ciphertext, signature)

print(f'Cipher text: {ciphertext}')
print(f'Signature: {signature}')

if plaintext:
    print(f'Plain text: {plaintext}')
else:
    print('Could not decrypt the message.')

if signature:
    print('Signature verified')
else:
    print('Could not verify the message signature')
"""
