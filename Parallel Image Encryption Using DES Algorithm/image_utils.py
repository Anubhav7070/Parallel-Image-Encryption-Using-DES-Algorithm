# image_utils.py
import numpy as np # type: ignore
import cv2 # type: ignore
from PIL import Image # type: ignore
import io

def load_image(image_path):
    """Load an image file and return as a numpy array."""
    return cv2.imread(image_path)

def save_image(image_array, output_path):
    """Save a numpy array as an image file."""
    cv2.imwrite(output_path, image_array)

def image_to_blocks(image, block_size=64):
    """
    Split an image into blocks for parallel processing.
    Returns a list of blocks and the original image shape.
    """
    # Convert image to flat byte array
    image_bytes = image.tobytes()
    
    # Calculate number of blocks
    block_size_bytes = block_size  # block_size in bytes
    num_blocks = (len(image_bytes) + block_size_bytes - 1) // block_size_bytes
    
    # Split into blocks
    blocks = []
    for i in range(num_blocks):
        start = i * block_size_bytes
        end = min(start + block_size_bytes, len(image_bytes))
        block = image_bytes[start:end]
        blocks.append(block)
    
    return blocks, image.shape

def blocks_to_image(blocks, original_shape):
    """
    Reconstruct an image from a list of blocks.
    """
    # Combine all blocks into a single byte array
    image_bytes = b''.join(blocks)
    
    # Convert back to numpy array with original shape
    flat_array = np.frombuffer(image_bytes, dtype=np.uint8)
    
    # Ensure we have the right number of bytes
    expected_size = original_shape[0] * original_shape[1] * original_shape[2]
    if len(flat_array) >= expected_size:
        flat_array = flat_array[:expected_size]
    else:
        # Pad with zeros if needed
        padding = np.zeros(expected_size - len(flat_array), dtype=np.uint8)
        flat_array = np.concatenate([flat_array, padding])
    
    # Reshape to original image dimensions
    image_array = flat_array.reshape(original_shape)
    
    return image_array