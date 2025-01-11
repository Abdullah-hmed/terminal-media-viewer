A Python package for viewing media files in the terminal as Unicode/ASCII art.

# Installation
To install the terminal-media-viewer package, run the following commands:

Clone the repository

```bash
git clone https://github.com/Abdullah-hmed/terminal-media-viewer.git
cd terminal-media-viewer
```
Install the package locally:

```bash
pip install .
```
# Usage
To use the terminal-media-viewer package, simply run the following command:

```bash
mediaviewer <media_file>
```
Replace <media_file> with the path to the media file you want to view.

# Arguments

| Argument | Description |
|----------|-------------|
| -w, --width | Width of the ASCII art (default: 80) |
| -bw, --black-white | Color the image (default: false) |


# Example
To view a video file called example.mp4, run the following command:

```bash
mediaviewer example.mp4 # Will play the video in the terminal in color
```
With Arguments:

```bash
mediaviewer -w 100 example.mp4  # Will set video width to 100
mediaviewer -bw example.mp4   # Will play the video in the terminal using unicode blocks
```

# License
This project is released under the [MIT License](https://choosealicense.com/licenses/mit/).