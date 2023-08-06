from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "emojiswitch",
    version = "0.0.2",
    keywords = ("pip", "emojiswitch", "meiqihezi"),
    description = "emoji switch",
    long_description = "emoji switch supporting Chinese and English",
    long_description_content_type='',
    python_requires=">=3.6.0",
    license = "",

    url = "",
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
