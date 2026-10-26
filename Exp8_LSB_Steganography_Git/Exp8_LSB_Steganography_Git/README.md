# Experiment 8 — LSB Image Steganography

**Student:** Bibin Alex Tom  
**Roll No.:** 8

This program hides a text message in the least significant bits of RGB pixels and extracts it again.

## Files
- `lsb_stego.py` — Python program
- `cover.png` — sample cover image
- `requirements.txt` — Pillow dependency

## Commands

Install the dependency:
```bash
python -m pip install -r requirements.txt
```

Hide a message (reads `cover.png`, creates `out.png`):
```bash
python lsb_stego.py hide "secret"
```

Extract the message:
```bash
python lsb_stego.py extract out.png
```

Expected output:
```text
Message hidden successfully in out.png
Extracted message: secret
```

Use PNG images; JPEG compression can destroy LSB-encoded data. Only use images you own or have permission to modify.
