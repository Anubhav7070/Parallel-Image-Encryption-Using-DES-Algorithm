# parallel_des.py
import multiprocessing
import time
import numpy as np # type: ignore
from des_utils import get_des_key, encrypt_block, decrypt_block
from image_utils import load_image, save_image, image_to_blocks, blocks_to_image
import matplotlib.pyplot as plt # type: ignore
import os

def encrypt_image_parallel(image_path, key_str, output_path, block_size=64, num_processes=None):
    """
    Encrypt an image using DES algorithm with parallel processing.
    
    Parameters:
    - image_path: Path to the input image
    - key_str: Encryption key (string or bytes)
    - output_path: Path to save the encrypted image
    - block_size: Size of blocks for processing (in bytes)
    - num_processes: Number of processes to use (defaults to CPU count)
    
    Returns:
    - Time taken for encryption
    """
    start_time = time.time()
    
    # Load the image
    image = load_image(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    
    # Prepare the key
    key = get_des_key(key_str)
    
    # Split the image into blocks
    blocks, original_shape = image_to_blocks(image, block_size)
    
    # Prepare data for parallel processing
    process_data = [(block, key) for block in blocks]
    
    # Set up multiprocessing pool
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    # Process blocks in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        encrypted_blocks = pool.map(encrypt_block, process_data)
    
    # Save the encrypted data
    with open(output_path, 'wb') as f:
        # Save original image shape for decryption
        shape_data = np.array(original_shape, dtype=np.int32).tobytes()
        f.write(len(shape_data).to_bytes(4, byteorder='big'))
        f.write(shape_data)
        
        # Save encrypted blocks
        for block in encrypted_blocks:
            block_size_bytes = len(block).to_bytes(4, byteorder='big')
            f.write(block_size_bytes)
            f.write(block)
    
    end_time = time.time()
    encryption_time = end_time - start_time
    
    return encryption_time

def decrypt_image_parallel(encrypted_path, key_str, output_path, num_processes=None):
    """
    Decrypt an image using DES algorithm with parallel processing.
    
    Parameters:
    - encrypted_path: Path to the encrypted image
    - key_str: Decryption key (string or bytes)
    - output_path: Path to save the decrypted image
    - num_processes: Number of processes to use (defaults to CPU count)
    
    Returns:
    - Time taken for decryption
    """
    start_time = time.time()
    
    # Prepare the key
    key = get_des_key(key_str)
    
    # Read the encrypted data
    with open(encrypted_path, 'rb') as f:
        # Read original image shape
        shape_size = int.from_bytes(f.read(4), byteorder='big')
        shape_data = f.read(shape_size)
        original_shape = tuple(np.frombuffer(shape_data, dtype=np.int32))
        
        # Read encrypted blocks
        encrypted_blocks = []
        while True:
            block_size_bytes = f.read(4)
            if not block_size_bytes:
                break
            
            block_size = int.from_bytes(block_size_bytes, byteorder='big')
            block = f.read(block_size)
            encrypted_blocks.append(block)
    
    # Prepare data for parallel processing
    process_data = [
        (block, key, original_shape, i == len(encrypted_blocks) - 1) 
        for i, block in enumerate(encrypted_blocks)
    ]
    
    # Set up multiprocessing pool
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    # Process blocks in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        decrypted_blocks = pool.map(decrypt_block, process_data)
    
    # Reconstruct the image
    image_array = blocks_to_image(decrypted_blocks, original_shape)
    
    # Save the decrypted image
    save_image(image_array, output_path)
    
    end_time = time.time()
    decryption_time = end_time - start_time
    
    return decryption_time

def plot_performance_comparison(sequential_time, parallel_times, core_counts):
    """
    Plot performance comparison between sequential and parallel processing.
    
    Parameters:
    - sequential_time: Time taken for sequential processing
    - parallel_times: List of times taken for parallel processing with different core counts
    - core_counts: List of core counts used for parallel processing
    """
    plt.figure(figsize=(10, 6))
    
    # Calculate speedups
    speedups = [sequential_time / p_time for p_time in parallel_times]
    
    # Bar chart
    bars = plt.bar(range(len(core_counts) + 1), [1.0] + speedups, color=['gray'] + ['blue'] * len(core_counts))
    plt.xticks(range(len(core_counts) + 1), ['Sequential'] + [f'{c} Cores' for c in core_counts])
    plt.ylabel('Speedup (relative to sequential)')
    plt.title('DES Image Encryption Performance Comparison')
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.2f}x', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    plt.close()
    