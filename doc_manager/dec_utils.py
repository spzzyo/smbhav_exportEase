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

def decrypt_and_verify_document(s3_encrypted_key, s3_metadata_key):
    """Decrypt and verify a document using dynamically retrieved keys and metadata."""

    # Step 1: Download encrypted file and metadata
    encrypted_path = "temp_encrypted_file"
    metadata_path = "temp_metadata.txt"
    s3_client.download_file(S3_BUCKET_NAME, s3_encrypted_key, encrypted_path)
    s3_client.download_file(S3_BUCKET_NAME, s3_metadata_key, metadata_path)

    # Step 2: Read metadata
    with open(metadata_path, "r") as f:
        metadata = eval(f.read())

    # Step 3: Decrypt AES key
    aes_key = base64.b64decode(metadata["aes_key"])

    # Step 4: Decrypt document
    decrypted_path = decrypt_document(encrypted_path, aes_key)

    # Step 5: Verify signature
    signature = bytes.fromhex(metadata["signature"])
    with open(f"keys/{os.path.basename(s3_metadata_key).split('_')[0]}_public.pem", "rb") as f:
        public_key_pem = f.read()
    with open(encrypted_path, "rb") as f:
        encrypted_content = f.read()
    # if not verify_signature(encrypted_content, signature, public_key_pem):
    #     raise ValueError("Signature verification failed.")
    
    if verify_signature(encrypted_content, signature, public_key_pem):
        raise ValueError("Signature verification failed.")


    # Cleanup
    os.remove(encrypted_path)
    os.remove(metadata_path)

    return decrypted_path