import os 
from setuptools import setup

__version__ = None
here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, "disctext", "version.py")).read())

setup(
    name = "disctext",
    version = __version__,
    packages = ["disctext"],
    author = "Akbar Amin",
    author_email = "akbar.amin917@gmail.com",
    url = "https://github.com/akbar-amin/disctext",
    description = "A tool for creating ASCII art and sharing it on Discord.",
    keywords = ["discord", "ascii", "art"], 
    license="MIT License",
    install_requires = ["discord.py", "opencv_python", "numpy"]
)
