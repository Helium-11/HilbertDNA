# HilbertDNA
HilbertDNA  A reversible DNA-to-image codec using a Hilbert space-filling curve for deterministic steganographic encoding.  HilbertDNA converts text into a DNA sequence, packs it into image pixels using Hilbert traversal, and allows full recovery of the original text without loss.

## Overview
TEXT
→ UTF-8 BYTES
→ BINARY
→ DNA (2-bit encoding)
→ IMAGE (Hilbert curve mapping)
→ DNA
→ BINARY
→ UTF-8 BYTES
→TEXT
