from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cloze-sdk",
    version="1.0.0",
    author="Cloze SDK",
    description="Python SDK for the Cloze API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloze/cloze-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    license="AGPLv3",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
)

