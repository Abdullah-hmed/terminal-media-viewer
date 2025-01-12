from PIL import Image
import os, time, shutil
import numpy as np
import imageio as iio
import argparse
import sys
import signal
import cv2
import yt_dlp
import re
import urllib.request


ascii_chars = ' ▁▂▃▄▅▆▇█'
media_playing = True

def handleSignal(signum, frame):
    sys.stdout.write('\033[?25h') # Show cursor again
    sys.exit(0)

def image_to_unicode(frame, colored=True, new_width=80):
    
    terminal_width, terminal_height = shutil.get_terminal_size()
    
    img = Image.fromarray(frame).convert("RGB") if colored else Image.fromarray(frame).convert("L")
    
    offset = 1 if not colored else 2

    # Resize image to fit terminal dimensions
    width, height = img.size
    aspect_ratio = height / width
    if new_width is None:
        new_width = terminal_width
    new_height = int(new_width * aspect_ratio * 0.55)
    if new_height > terminal_height:
        new_height = terminal_height - offset # Subtracting offset for the progress bar
        new_width = int(new_height / (aspect_ratio * 0.55))
    resized_img = img.resize((new_width, new_height))

    if colored:
        # If colored, map pixels to colored unicode
        result = []
        for y in range(new_height):
            for x in range(new_width):
                result.append(rgb_pixel(*resized_img.getpixel((x,y))))
            result.append('\n')
        return ''.join(result)
    else:
        # If not colored, map pixels to simple unicode array
        pixels = resized_img.getdata()
        ascii_str = ''.join([ascii_chars[pixel // 32] for pixel in pixels])

        # Format the unicode string
        ascii_img = '\n'.join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
        return ascii_img

def rgb_pixel(r, g, b):
    return f"\033[38;2;{r};{g};{b}m█\033[0m"

def high_res_image_to_unicode(frame, new_width=80):
    img = Image.fromarray(frame).convert("RGB")
    terminal_width, terminal_height = shutil.get_terminal_size()

    width, height = img.size
    aspect_ratio = height / width
    if new_width is None:
        new_width = terminal_width
    
    new_height = int(new_width * aspect_ratio * 0.55) * 2
    if new_height > terminal_height * 2:  # Double height since doubling resolution
        new_height = (terminal_height - 2) * 2
        new_width = int(new_height / (aspect_ratio * 0.55 * 2))
    resized_img = img.resize((new_width, new_height))
    
    result = []
    for y in range(0, new_height - 1, 2):
        for x in range(new_width):
            
            top_pixel = resized_img.getpixel((x, y))
            bottom_pixel = resized_img.getpixel((x, y + 1))
            
            # Create half blocks with different colors for top and bottom
            result.append(high_res_rgb_pixels(top_pixel, bottom_pixel))
        result.append('\n')
    
    return ''.join(result)

def high_res_rgb_pixels(upper_pixel, lower_pixel):
    return f"\033[38;2;{upper_pixel[0]};{upper_pixel[1]};{upper_pixel[2]}m\033[48;2;{lower_pixel[0]};{lower_pixel[1]};{lower_pixel[2]}m▀\033[0m"

def video_to_unicode(video_path, width=80, frame_rate=24, colored=True, high_resolution=False):
    
    sys.stdout.write('\033[?25l')  # Hide the cursor

    video_reader = iio.get_reader(video_path)
    if not video_path.endswith('.gif'):
        frame_count = video_reader.count_frames()
    
    current_frame = 1
    first_frame = True
    for frame in video_reader:
        
        
        if colored:
            # If colored, map pixels to colored unicode
            unicode_frame = high_res_image_to_unicode(frame, new_width=width) if high_resolution else image_to_unicode(frame, colored=True, new_width=width)
        else:
            unicode_frame = image_to_unicode(frame, colored=False, new_width=width)
        
        
        if first_frame:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write('\033[s')  # Save position
            print(unicode_frame, end='', flush=True)
            first_frame = False
        else: 
            sys.stdout.write('\033[u')  # Getting to initial position
            print(unicode_frame, end='', flush=True)
        
        
        if not video_path.endswith('.gif'):
            progress_bar(current_frame, frame_count, width, play_icon='▎▎')
        current_frame += 1
        time.sleep(1 / frame_rate)
        
    sys.stdout.write('\033[?25h') # Show cursor again

def url_to_unicode(url, width=80, frame_rate=24, colored=True, high_resolution=False):
    
    sys.stdout.write('\033[?25l')  # Hide the cursor

    # Open the video stream from URL using cv2
    cap = cv2.VideoCapture(url)
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    
    # Get frame count and FPS
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    current_frame = 0
    first_frame = True
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if no frame is read (video ended or error)
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        if colored:
            unicode_frame = (
                high_res_image_to_unicode(frame_rgb, new_width=width)
                if high_resolution else
                image_to_unicode(frame_rgb, colored=True, new_width=width)
            )
        else:
            unicode_frame = image_to_unicode(frame_rgb, colored=False, new_width=width)
        
        if first_frame:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write('\033[s')  # Save position
            print(unicode_frame, end='', flush=True)
            first_frame = False
        else:
            sys.stdout.write('\033[u')  # Restore to initial position
            print(unicode_frame, end='', flush=True)
        
        current_frame += 1
        progress_bar(current_frame, frame_count, width, play_icon='▎▎')
        
        # Sleep to match the desired frame rate
        time.sleep(1 / frame_rate)
    
    cap.release()  # Release the video capture object
    sys.stdout.write('\033[?25h')  # Show the cursor again


def progress_bar(current, total, bar_length, play_icon='▎▎'):
    bar_length = int(bar_length) - 10
    filled_length = int(round(bar_length * current / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\n {play_icon} |{bar}| {current}/{total}', end='')

    if current == total:
        print()

def handle_online_image(url, width, colored, high_res):
    
    urllib.request.urlretrieve(url, "online_image")
    img = Image.open("online_image")
    frame = np.array(img)
    ascii_art = high_res_image_to_unicode(frame, width) if high_res else image_to_unicode(frame, colored, width)
    os.remove("online_image")
    return ascii_art

def get_video_info(url):
    ydl_opts = {
        'quiet': True,  # Suppress the output
        'no_warnings': True,  # Suppress warnings
        'noplaylist': True,  # Only process the single video, not a playlist
        'format': '133+139'  # 136: 720p video, 140: AAC audio
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        best_format = info['formats'][-1]  # Get the selected format
        video_url = best_format['url']  
        fps = best_format.get('fps', 'N/A')  # Default to 'N/A' if fps is not found

        return video_url, fps


def main():
    
    signal.signal(signal.SIGINT, handleSignal)

    parser = argparse.ArgumentParser(description='Convert an image or video to UNICODE art.')
    parser.add_argument('input_path', type=str, help='Path to the image or video file')
    parser.add_argument('-w', '--width', type=int, default=80, help='Width of the ASCII art (default: 80)')
    parser.add_argument('-bw', '--black-white', dest='grayscale', action='store_true', help='Display media as grayscale')
    parser.add_argument('-hr', '--high-resolution', dest='high_resolution', action='store_true', help='High resolution rendering')

    args = parser.parse_args()

    try:
        colored = not args.grayscale
        high_res = args.high_resolution
        # is_url = args.input_path.startswith('http://') or args.input_path.startswith('https://')
        is_url = bool(re.match(r'https?://\S+', args.input_path))

        is_image = args.input_path.endswith(tuple(Image.registered_extensions().keys()))
        if args.grayscale and args.high_resolution:
            print("Error: High resolution rendering is not compatible with grayscale mode.")
            sys.exit(1)

        elif is_url:
            # URL
            if is_image:
                
                image = handle_online_image(args.input_path, args.width, colored, high_res)
                print(image)
                
            else:
                
                if 'youtu' in args.input_path:
                    yt_url, fps = get_video_info(args.input_path)
                    
                    if fps != 'N/A':
                        url_to_unicode(yt_url, width=args.width, colored=colored, frame_rate=int(fps), high_resolution=high_res)
                    else:
                        url_to_unicode(yt_url, width=args.width, colored=colored, high_resolution=high_res)
                else:
                    url_to_unicode(args.input_path, width=args.width, colored=colored, high_resolution=high_res)

        else:
            # Local file
            if is_image:
                
                img = Image.open(args.input_path)
                frame = np.array(img)
                ascii_art = high_res_image_to_unicode(frame, args.width) if high_res else image_to_unicode(frame, colored, args.width)
                print(ascii_art)
                
            else:
                
                video_to_unicode(args.input_path, colored=colored, width=args.width, high_resolution=high_res)
                
    except FileNotFoundError:
        print(f"Error: File '{args.input_path}' not found.")
    except ValueError:
        print(f"Error: Invalid width value '{args.width}'. Please provide a positive integer.")

if __name__ == "__main__":
    main()