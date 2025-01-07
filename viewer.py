from PIL import Image
import argparse

# ASCII characters by brightness
ascii_chars = ' ▁▂▃▄▅▆▇█'

def image_to_ascii(image_path, new_width=80):
    # Open the image
    img = Image.open(image_path)

    
    grayscale_img = img.convert("L")

    # Resize image
    width, height = grayscale_img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    resized_img = grayscale_img.resize((new_width, new_height))

    # Map pixels to ASCII
    pixels = resized_img.getdata()
    ascii_str = ''.join([ascii_chars[pixel // 32] for pixel in pixels])

    # Format the ASCII string
    ascii_img = '\n'.join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
    return ascii_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert an image to ASCII art.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('-w', '--width', type=int, default=60, help='Width of the ASCII art (default: 60)')

    args = parser.parse_args()

    try:
        ascii_art = image_to_ascii(args.image_path, args.width)
        print(ascii_art)
    except FileNotFoundError:
        print(f"Error: Image file '{args.image_path}' not found.")
    except ValueError:
        print(f"Error: Invalid width value '{args.width}'. Please provide a positive integer.")
