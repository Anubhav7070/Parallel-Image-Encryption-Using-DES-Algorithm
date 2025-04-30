# main.py
import os
import time
import multiprocessing
from parallel_des import encrypt_image_parallel, decrypt_image_parallel, plot_performance_comparison

def run_sequential_des(image_path, key_str, encrypted_path, decrypted_path):
    """Run DES encryption/decryption sequentially for comparison."""
    from des_utils import get_des_key, encrypt_block, decrypt_block
    from image_utils import load_image, save_image, image_to_blocks, blocks_to_image
    import numpy as np # type: ignore
    
    start_time = time.time()
    
    # Load the image
    image = load_image(image_path)
    
    # Prepare the key
    key = get_des_key(key_str)
    
    # Split the image into blocks
    blocks, original_shape = image_to_blocks(image)
    
    # Process blocks sequentially
    encrypted_blocks = []
    for block in blocks:
        encrypted_block = encrypt_block((block, key))
        encrypted_blocks.append(encrypted_block)
    
    # Save the encrypted data (similar to parallel version)
    with open(encrypted_path, 'wb') as f:
        # Save original image shape for decryption
        shape_data = np.array(original_shape, dtype=np.int32).tobytes()
        f.write(len(shape_data).to_bytes(4, byteorder='big'))
        f.write(shape_data)
        
        # Save encrypted blocks
        for block in encrypted_blocks:
            block_size_bytes = len(block).to_bytes(4, byteorder='big')
            f.write(block_size_bytes)
            f.write(block)
    
    encryption_time = time.time() - start_time
    
    return encryption_time

def main():
    # Define parameters
    image_path = "test_image.jpg"  # Place a test image in the same directory
    key_str = "mysecret"
    encrypted_path = "encrypted_image.bin"
    decrypted_path = "decrypted_image.jpg"
    
    # Ensure test image exists
    if not os.path.exists(image_path):
        print(f"Please place a test image named '{image_path}' in the same directory.")
        return
    
    # Get available CPU cores
    max_cores = multiprocessing.cpu_count()
    print(f"Running on a system with {max_cores} CPU cores")
    
    # Run sequential version for comparison
    print("Running sequential DES encryption for comparison...")
    sequential_time = run_sequential_des(image_path, key_str, "sequential_encrypted.bin", "sequential_decrypted.jpg")
    print(f"Sequential encryption time: {sequential_time:.2f} seconds")
    
    # Test with different numbers of cores
    core_counts = [1, 2, max(2, max_cores//2), max_cores]
    core_counts = sorted(list(set(core_counts)))  # Remove duplicates and sort
    
    parallel_times = []
    for cores in core_counts:
        print(f"\nTesting with {cores} cores:")
        
        # Encrypt the image
        print(f"Encrypting image: {image_path}")
        encryption_time = encrypt_image_parallel(image_path, key_str, encrypted_path, num_processes=cores)
        print(f"Encryption time: {encryption_time:.2f} seconds")
        
        # Decrypt the image
        print(f"Decrypting to: {decrypted_path}")
        decryption_time = decrypt_image_parallel(encrypted_path, key_str, decrypted_path, num_processes=cores)
        print(f"Decryption time: {decryption_time:.2f} seconds")
        print(f"Total processing time: {encryption_time + decryption_time:.2f} seconds")
        
        parallel_times.append(encryption_time)
    
    # Plot performance comparison
    plot_performance_comparison(sequential_time, parallel_times, core_counts)
    print("\nPerformance comparison plot saved as 'performance_comparison.png'")
    
    print("\nDone! Check the output files.")

if __name__ == "__main__":
    main()