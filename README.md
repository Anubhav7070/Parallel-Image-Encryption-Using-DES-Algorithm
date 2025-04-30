
# Parallel Image Encryption Using DES Algorithm

## 📘 Overview

This project presents an implementation of image encryption using the **Data Encryption Standard (DES)** algorithm in Python. To enhance encryption performance, the project leverages **parallel computing** via Python’s `multiprocessing` module, enabling faster processing of large image files by utilizing multiple CPU cores.

This system is designed for educational purposes and experimental cryptographic research, especially for real-time or large-scale image security scenarios.

---

## 🧠 Key Features

- **Symmetric DES-based encryption** of image data.
- **Parallel processing** using Python's `multiprocessing` to improve speed.
- **Lossless decryption** to accurately reconstruct the original image.
- Performance benchmarking against sequential execution.
- Support for colored and grayscale images.
- Simple and cross-platform implementation (tested on Windows).

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Libraries:**
  - `OpenCV` for image manipulation
  - `PyCryptodome` for DES cryptographic functions
  - `multiprocessing` for parallel execution
  - `NumPy` for data processing
  - `Matplotlib` for performance graphing

---

## 📁 Project Structure

```
project/
│
├── main.py                     # Entry point for running and comparing encryption
├── des_utils.py                # DES key and block encryption/decryption utilities
├── image_utils.py              # Image loading, saving, block splitting/joining
├── parallel_des.py             # Parallel image encryption/decryption logic
├── test_multiprocessing.py     # Benchmark script for multiprocessing test
├── test_image.jpg              # Sample input image
├── encrypted_image.bin         # Output encrypted binary file
├── decrypted_image.jpg         # Output decrypted image
└── performance_comparison.png  # Speedup chart
```

---

## 🚀 How to Run

### 🖥️ Requirements

Install the dependencies:

```bash
pip install opencv-python pycryptodome matplotlib pillow
```

### ▶️ Execution

1. Place an image file named `test_image.jpg` in the root directory.
2. Run the project using:

```bash
python main.py
```

This will:
- Perform DES encryption on the image sequentially and in parallel.
- Output performance comparison.
- Save the results including:
  - `encrypted_image.bin` (binary output),
  - `decrypted_image.jpg` (reconstructed image),
  - `performance_comparison.png` (visual speedup chart).

---

## 📊 Results

| Image Size  | Sequential Time (s) | Parallel Time (s) | Speedup |
|-------------|---------------------|--------------------|---------|
| 256×256     | 1.25                | 0.72               | ~1.74×  |
| 512×512     | 5.89                | 2.43               | ~2.42×  |
| 1024×1024   | 24.76               | 9.85               | ~2.51×  |

---

## ✅ Advantages

- Enhanced speed through multiprocessing.
- Modular and clean Python implementation.
- Ready for future improvements like GPU support or cloud deployment.

---

## 🔒 Limitations

- DES is outdated for high-security contexts.
- Not suitable for commercial cryptographic applications.


## 📜 License

This project is intended for academic and educational use only.
