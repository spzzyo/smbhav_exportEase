from Crypto.Cipher import AES
from ecdsa import VerifyingKey
import base64
import hashlib
import boto3
import os 

# AWS S3 setup
s3_client = boto3.client('s3')
S3_BUCKET_NAME = "secure-doc-bucket"

def verify_signature(content, signature, public_key_pem):
    """Verify the document's signature."""
    public_key = VerifyingKey.from_pem(public_key_pem)
    document_hash = hashlib.sha256(content).digest()
    return public_key.verify(signature, document_hash)

def decrypt_document(encrypted_path, aes_key):
    """Decrypt the document using AES."""
    with open(encrypted_path, "rb") as f:
        nonce, ciphertext, tag = f.read(16), f.read(), f.read(16)
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    decrypted_path = "decrypted_" + os.path.basename(encrypted_path)
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)
    return decrypted_path

def retrieve_metadata_from_s3(metadata_s3_key):
    """Retrieve metadata from S3."""
    metadata_path = "metadata.txt"
    s3_client.download_file(S3_BUCKET_NAME, metadata_s3_key, metadata_path)

    # Read metadata
    with open(metadata_path, "r") as f:
        metadata = eval(f.read())  # Use eval to convert string back to dictionary
    os.remove(metadata_path)
    return metadata

def decrypt_and_verify_document(encrypted_s3_key, metadata_s3_key):
    """Admin: Decrypt and verify document before sharing."""
    # Step 1: Download encrypted document and metadata from S3
    encrypted_path = "encrypted_document.pdf"
    s3_client.download_file(S3_BUCKET_NAME, encrypted_s3_key, encrypted_path)
    metadata = retrieve_metadata_from_s3(metadata_s3_key)

    # Step 2: Extract the AES key and signature
    aes_key = base64.b64decode(metadata["aes_key"])
    signature = bytes.fromhex(metadata["signature"])

    # Step 3: Verify the signature
    with open(encrypted_path, "rb") as f:
        encrypted_content = f.read()
    if verify_signature(encrypted_content, signature, public_key_pem):
        print("Document signature verified.")
    else:
        print("Document signature verification failed.")
        return

    # Step 4: Decrypt the document
    decrypted_path = decrypt_document(encrypted_path, aes_key)
    print("Decrypted document saved at:", decrypted_path)

    # Optionally: Delete the encrypted document after decryption
    os.remove(encrypted_path)
