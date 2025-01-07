from setuptools import setup

setup(
    name="terminal-media-viewer",
    version="1.0.0",
    py_modules=["viewer"],
    entry_points={
        "console_scripts": [
            "mediaviewer=viewer:main",
        ],
    },
    install_requires=[
        'Pillow',
        'imageio',
        'numpy',
        'argparse',
    ],
    author="Abdullah Ahmed",
    description="python script to view media files in terminal as unicode/ascii art",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/abdullah-hmed/terminal-media-viewer',
    license='MIT',
    python_requires=">=3.6",
)