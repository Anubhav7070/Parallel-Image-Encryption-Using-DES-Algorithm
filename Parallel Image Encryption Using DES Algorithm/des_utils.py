# des_utils.py
from Crypto.Cipher import DES # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore
import numpy as np # type: ignore

def get_des_key(key_str):
    """Generate a valid DES key from a string."""
    # DES requires an 8-byte key
    if isinstance(key_str, str):
        key = key_str.encode('utf-8')
    else:
        key = key_str
    
    # Ensure the key is exactly 8 bytes
    if len(key) < 8:
        key = pad(key, 8)
    
    return key[:8]  # Take only the first 8 bytes

def encrypt_block(block_data):
    """Encrypt a single block of data using DES."""
    block, key = block_data
    
    # Convert to bytes if numpy array
    if isinstance(block, np.ndarray):
        block_bytes = block.tobytes()
    else:
        block_bytes = block
    
    # Ensure block size is a multiple of 8 bytes (DES block size)
    padded_block = pad(block_bytes, 8)
    
    # Create DES cipher
    cipher = DES.new(key, DES.MODE_ECB)
    
    # Encrypt
    encrypted_block = cipher.encrypt(padded_block)
    
    return encrypted_block

def decrypt_block(block_data):
    """Decrypt a single block of data using DES."""
    encrypted_block, key, original_shape, is_last = block_data
    
    # Create DES cipher
    cipher = DES.new(key, DES.MODE_ECB)
    
    # Decrypt
    decrypted_padded = cipher.decrypt(encrypted_block)
    
    # Remove padding if this is the last block
    if is_last:
        try:
            decrypted_data = unpad(decrypted_padded, 8)
        except ValueError:
            # If unpadding fails, just return the raw data
            decrypted_data = decrypted_padded
    else:
        decrypted_data = decrypted_padded
    
    return decrypted_data