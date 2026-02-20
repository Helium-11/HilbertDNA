# HilbertDNA
HilbertDNA  A reversible DNA-to-image codec using a Hilbert space-filling curve for deterministic steganographic encoding.  HilbertDNA converts text into a DNA sequence, packs it into image pixels using Hilbert traversal, and allows full recovery of the original text without loss.

## Overview

### Encoding  
TEXT
→ UTF-8 BYTES
→ BINARY
→ DNA (2-bit encoding)
→ IMAGE (Hilbert curve mapping)  

### Decoding
IMAGE (Hilbert curve mapping)
→ DNA
→ BINARY
→ UTF-8 BYTES
→TEXT
## Backend Architecture

### Python 3
+ Core language for all encoding/decoding logic  
+ Used for binary processing, DNA mapping, and Hilbert traversal  
+ Chosen for readability, correctness, and ecosystem maturity  

### Modular Design
+ `tex_to_dna.py` handles text ↔ binary ↔ DNA conversion  
+ `hilbert.py` handles DNA ↔ image encoding via Hilbert curve  
+ Clear separation of concerns for maintainability  
+ Logic isolated from interface (CLI / API ready)  

### Binary & Data Handling
+ UTF-8 safe encoding to support full Unicode  
+ 32-bit length header for deterministic decoding  
+ Byte packing (2 DNA bases per byte) for storage efficiency  
+ Explicit validation for corrupted or incomplete data  

---

## Web & API Readiness

### REST-Compatible Core Logic
+ Stateless functions (pure input → output processing)  
+ Easily wrapped with Flask / FastAPI / Django REST Framework  
+ Designed for POST-based encode/decode endpoints  

### File Handling
+ Supports text file → image generation workflows  
+ Supports image upload → text extraction workflows  
+ Compatible with multipart/form-data requests  

### Frontend Integration
+ Image output allows browser preview and downloads  
+ UTF-8 decoded output safe for web rendering  
+ Deterministic results for consistent frontend display  


---

## Future Web Extensions
 
+ JWT-based authentication  
+ Async background processing (Celery / Redis)  
+ Cloud storage integration (AWS S3 / GCP Storage)  
+ Docker containerization for deployment  
