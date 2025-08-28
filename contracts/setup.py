import os
from setuptools import setup, find_packages

setup(
    name="s2s-contracts",
    version="0.1.0",
    description="Shared API & event schemas for Seed to Shelf platform",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="LX Solutions",
    author_email="engineering@lxsolutions.com",
    url="https://github.com/lxsolutions/seed-to-shelf",
    packages=find_packages(),
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="food supply-chain traceability events schemas pydantic",
)