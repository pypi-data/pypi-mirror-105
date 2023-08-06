from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "emojiswitch",
    version = "0.0.3",
    keywords = ("pip", "emojiswitch", "meiqihezi"),
    description = "emoji switch",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6.0",
    license = "",

    url = "https://github.com/yuanhong18/emojiswitch",
    author = "meiqihezi",
    author_email = "18202722061@163.com",

    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    platforms = "any",

    scripts = [],
    entry_points = {
    }
)
