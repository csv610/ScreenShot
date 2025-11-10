from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="screenshot-py",
    version="1.0.0",
    author="csv610",
    author_email="",
    description="A Python utility for capturing screenshots with flexible options",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/csv610/ScreenShot",
    py_modules=["screenshot"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Editors",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=10.0.0",
    ],
)
