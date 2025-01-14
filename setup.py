from setuptools import setup

setup(
    name="terminal-media-viewer",
    version="1.0.0",
    py_modules=["viewer", "utils"],
    entry_points={
        "console_scripts": [
            "mediaviewer=viewer:main",
        ],
    },
    install_requires=[
        'Pillow',
        'imageio',
        'imageio-ffmpeg',
        'numpy',
        'argparse',
        'opencv-python==4.10.0.84',
        'yt-dlp==2024.12.23'
    ],
    author="Abdullah Ahmed",
    description="python script to view media files in terminal as unicode/ascii art",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/abdullah-hmed/terminal-media-viewer',
    license='MIT',
    python_requires=">=3.6",
)