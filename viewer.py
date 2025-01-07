from PIL import Image
import os, time, tqdm
import imageio as iio
import argparse


ascii_chars = ' ▁▂▃▄▅▆▇█'

def image_to_unicode(frame, new_width=80):
    
    img = Image.fromarray(frame).convert("L")

    # Resize image
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    resized_img = img.resize((new_width, new_height))

    # Map pixels to unicode
    pixels = resized_img.getdata()
    ascii_str = ''.join([ascii_chars[pixel // 32] for pixel in pixels])

    # Format the unicode string
    ascii_img = '\n'.join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
    return ascii_img

def video_to_unicode(video_path, width=80, frame_rate=24):
    frame_count = iio.get_reader(video_path).count_frames()
    
    video_reader = iio.imiter(video_path)
    current_frame = 0
    for frame in video_reader:
        unicode_frame = image_to_unicode(frame, new_width=width)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\r', unicode_frame)
        progress_bar(current_frame, frame_count, width)
        current_frame += 1
        time.sleep(1 / frame_rate)

def progress_bar(current, total, bar_length):
    bar_length = int(bar_length) - 10
    filled_length = int(round(bar_length * current / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\n|{bar}| {current}/{total}', end='')

    if current == total:
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert an image or video to UNICODE art.')
    parser.add_argument('input_path', type=str, help='Path to the image or video file')
    parser.add_argument('-w', '--width', type=int, default=60, help='Width of the ASCII art (default: 60)')
    parser.add_argument('-v', '--video', action='store_true', help='Input is a video file')

    args = parser.parse_args()

    try:
        if args.video:
            video_to_unicode(args.input_path, width=args.width)
        else:
            ascii_art = image_to_unicode(args.input_path, args.width)
            print(ascii_art)
    except FileNotFoundError:
        print(f"Error: File '{args.input_path}' not found.")
    except ValueError:
        print(f"Error: Invalid width value '{args.width}'. Please provide a positive integer.")