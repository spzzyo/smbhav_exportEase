from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from ecdsa import SECP256k1, SigningKey
from PIL import Image, ImageDraw, ImageFont
import os
import base64
import boto3
import hashlib

# AWS S3 setup
s3_client = boto3.client('s3')
S3_BUCKET_NAME = "secure-doc-bucket"

def add_watermark(document_path, watermark_text="Smbhav Secure Document"):
    """Add watermark to the document."""
    img = Image.open(document_path)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    text_position = (10, 10)
    draw.text(text_position, watermark_text, fill="grey", font=font)
    watermarked_path = "watermarked_" + os.path.basename(document_path)
    img.save(watermarked_path)
    return watermarked_path

def encrypt_document(document_path, aes_key):
    """Encrypt the document using AES."""
    with open(document_path, "rb") as f:
        data = f.read()
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted_path = "encrypted_" + os.path.basename(document_path)
    with open(encrypted_path, "wb") as f:
        f.write(cipher.nonce + ciphertext + tag)
    return encrypted_path

def generate_keys():
    """Generate ECDSA private and public keys."""
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    private_key_pem = private_key.to_pem()
    public_key_pem = public_key.to_pem()

    return private_key_pem, public_key_pem

def sign_content(content, private_key_pem):
    """Sign the content with the private key."""
    private_key = SigningKey.from_pem(private_key_pem)
    document_hash = hashlib.sha256(content).digest()
    signature = private_key.sign(document_hash)
    return signature, document_hash

def handle_document_upload(document_path, user_id, category_name):
    """Handle document upload, watermark, encryption, and upload to S3."""
    
    # Step 1: Add watermark
    watermarked_path = add_watermark(document_path)
    print("Watermarked document created:", watermarked_path)

    # Step 2: Generate AES encryption key
    aes_key = get_random_bytes(16)
    print("AES Key Generated for encryption.")

    # Step 3: Encrypt the document
    encrypted_path = encrypt_document(watermarked_path, aes_key)
    print("Encrypted document created:", encrypted_path)

    # Step 4: Sign the encrypted document
    private_key, public_key = generate_keys()
    with open(encrypted_path, "rb") as f:
        encrypted_content = f.read()
    signature, document_hash = sign_content(encrypted_content, private_key)
    print("Document signed successfully.")

    # Step 5: Upload encrypted file to S3
    # Construct file paths for S3
    s3_encrypted_key = f"encrypted_docs/{category_name}/{os.path.basename(encrypted_path)}_{user_id}.pdf"
    s3_metadata_key = f"metadata/{category_name}/{os.path.basename(encrypted_path)}_{user_id}_metadata.txt"

    # Store the metadata (signature and hash) in a text file
    metadata = {
        "signature": signature.hex(),
        "hash": document_hash.hex(),
        "aes_key": base64.b64encode(aes_key).decode()  # base64 encode AES key
    }
    metadata_path = "metadata.txt"
    with open(metadata_path, "w") as f:
        f.write(str(metadata))
    
    # Upload the files to S3
    s3_client.upload_file(encrypted_path, S3_BUCKET_NAME, s3_encrypted_key)
    s3_client.upload_file(metadata_path, S3_BUCKET_NAME, s3_metadata_key)
    
    print("Files uploaded to S3 successfully.")

    # Clean up local metadata file
    os.remove(metadata_path)
    os.remove(encrypted_path)
    os.remove(watermarked_path)
