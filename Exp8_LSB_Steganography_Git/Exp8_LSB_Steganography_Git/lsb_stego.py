"""Experiment 8: LSB image steganography."""
import argparse
from PIL import Image


def hide(message, source="cover.png", destination="out.png"):
    image = Image.open(source).convert("RGB")
    payload = message.encode("utf-8")
    data = len(payload).to_bytes(4, "big") + payload
    bits = "".join(f"{byte:08b}" for byte in data)
    pixels = list(image.getdata())
    if len(bits) > len(pixels) * 3:
        raise ValueError("Message is too large for this image.")

    result = []
    index = 0
    for pixel in pixels:
        channels = []
        for channel in pixel:
            if index < len(bits):
                channel = (channel & 254) | int(bits[index])
                index += 1
            channels.append(channel)
        result.append(tuple(channels))

    image.putdata(result)
    image.save(destination, format="PNG")
    print(f"Message hidden successfully in {destination}")


def extract(source):
    image = Image.open(source).convert("RGB")
    bits = "".join(str(channel & 1) for pixel in image.getdata() for channel in pixel)
    if len(bits) < 32:
        raise ValueError("Image is too small or has no valid hidden message.")
    length = int(bits[:32], 2)
    end = 32 + length * 8
    if end > len(bits):
        raise ValueError("No complete hidden message found.")
    message = bytes(int(bits[i:i+8], 2) for i in range(32, end, 8))
    print("Extracted message:", message.decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="LSB image steganography")
    sub = parser.add_subparsers(dest="action", required=True)
    hp = sub.add_parser("hide", help="Hide a message in cover.png")
    hp.add_argument("message")
    hp.add_argument("--input", default="cover.png")
    hp.add_argument("--output", default="out.png")
    ep = sub.add_parser("extract", help="Extract a hidden message")
    ep.add_argument("image")
    args = parser.parse_args()
    try:
        if args.action == "hide":
            hide(args.message, args.input, args.output)
        else:
            extract(args.image)
    except (OSError, ValueError, UnicodeDecodeError) as err:
        parser.error(str(err))


if __name__ == "__main__":
    main()
