from PIL import Image
import os, time, shutil
import numpy as np
import imageio as iio
import argparse
import sys
import signal


ascii_chars = ' ▁▂▃▄▅▆▇█'

def handleSignal(signum, frame):
    sys.stdout.write('\033[?25h') # Show cursor again
    sys.exit(0)

def image_to_unicode(frame, new_width=80):
    
    terminal_width, terminal_height = shutil.get_terminal_size()
    
    img = Image.fromarray(frame).convert("L")

    # Resize image to fit terminal dimensions
    width, height = img.size
    aspect_ratio = height / width
    if new_width is None:
        new_width = terminal_width
    new_height = int(new_width * aspect_ratio * 0.55)
    if new_height > terminal_height:
        new_height = terminal_height - 1 # Subtracting 1 for the progress bar
        new_width = int(new_height / (aspect_ratio * 0.55))
    resized_img = img.resize((new_width, new_height))

    # Map pixels to unicode
    pixels = resized_img.getdata()
    ascii_str = ''.join([ascii_chars[pixel // 32] for pixel in pixels])

    # Format the unicode string
    ascii_img = '\n'.join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
    return ascii_img

def colored_image_to_unicode(frame, new_width=80):
    
    img = Image.fromarray(frame).convert("RGB")
    terminal_width, terminal_height = shutil.get_terminal_size()

    # Resize image to fit terminal dimensions
    width, height = img.size
    aspect_ratio = height / width
    if new_width is None:
        new_width = terminal_width
    new_height = int(new_width * aspect_ratio * 0.55)
    if new_height > terminal_height:
        new_height = terminal_height - 2 # Subtracting 2 for the progress bar
        new_width = int(new_height / (aspect_ratio * 0.55))
    resized_img = img.resize((new_width, new_height))
    
    result = []
    for y in range(new_height):
        for x in range(new_width):
            pixel = resized_img.getpixel((x,y))
            values = pixel
            result.append(rgb_pixel(*values))
        result.append('\n')
    return ''.join(result)

def rgb_pixel(r, g, b):
    return f"\033[38;2;{r};{g};{b}m█\033[0m"

def video_to_unicode(video_path, width=80, frame_rate=24, colored=True):
    
    sys.stdout.write('\033[?25l')  # Hide the cursor

    video_reader = iio.get_reader(video_path)
    if not video_path.endswith('.gif'):
        frame_count = video_reader.count_frames()
    
    current_frame = 1
    first_frame = True
    for frame in video_reader:
        
        # Color the image if needed
        if colored:
            unicode_frame = colored_image_to_unicode(frame, new_width=width)
        else:
            unicode_frame = image_to_unicode(frame, new_width=width)
        
        
        if first_frame:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write('\033[s')  # Save position
            print(unicode_frame, end='', flush=True)
            first_frame = False
        else: 
            sys.stdout.write('\033[u')  # Getting to initial position
            print(unicode_frame, end='', flush=True)
        
        
        if not video_path.endswith('.gif'):
            progress_bar(current_frame, frame_count, width)
        current_frame += 1
        time.sleep(1 / frame_rate)
        
    sys.stdout.write('\033[?25h') # Show cursor again


def progress_bar(current, total, bar_length):
    bar_length = int(bar_length) - 10
    filled_length = int(round(bar_length * current / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\n|{bar}| {current}/{total}', end='')

    if current == total:
        print()

def main():
    
    signal.signal(signal.SIGINT, handleSignal)

    parser = argparse.ArgumentParser(description='Convert an image or video to UNICODE art.')
    parser.add_argument('input_path', type=str, help='Path to the image or video file')
    parser.add_argument('-w', '--width', type=int, default=60, help='Width of the ASCII art (default: 60)')
    parser.add_argument('-gray', '--grayscale', action='store_false', help='Color the image')

    args = parser.parse_args()

    try:
        if args.input_path.endswith(('.mp4', '.gif', '.webm', '.mov', 'mkv')):
            video_to_unicode(args.input_path, width=args.width, colored=args.grayscale)
        else:
            img = Image.open(args.input_path)
            frame = np.array(img)
            colored = not args.grayscale
            if colored:
                ascii_art = image_to_unicode(frame, args.width)
            else:
                ascii_art = colored_image_to_unicode(frame, args.width)
            print(ascii_art)
    except FileNotFoundError:
        print(f"Error: File '{args.input_path}' not found.")
    except ValueError:
        print(f"Error: Invalid width value '{args.width}'. Please provide a positive integer.")

if __name__ == "__main__":
    main()