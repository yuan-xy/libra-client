import setuptools
from libra.version import version

with open("README.md", "r") as fh:
    content = fh.read()
    arr = content.split("\n")
    long_description = "\n".join(arr[3:])

setuptools.setup(
    name="libra-client",
    version=version,
    author="yuan xinyu",
    author_email="yuanxinyu.hangzhou@gmail.com",
    description="A python client for Libra network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuan-xy/libra-client.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'canoser>=0.2.0',
        'grpcio',
        'PyNaCl',
        'mnemonic'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)