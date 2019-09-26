import setuptools
import hashlib
from libra.version import version

with open("README.md", "r") as fh:
    content = fh.read()
    arr = content.split("\n")
    long_description = "\n".join(arr[3:5])

install_requires=[
        'canoser>=0.3.2',
        'protobuf',
        'grpcio',
        'PyNaCl',
        'requests',
        "toml",
        'mnemonic'
    ]

if not 'sha3-256' in hashlib.algorithms_available:
    install_requires.append("pysha3")

setuptools.setup(
    name="libra-client",
    version=version,
    author="yuan xinyu",
    author_email="yuanxinyu.hangzhou@gmail.com",
    description="A CLI inteface Libra client and Python API for Libra blockchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuan-xy/libra-client.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':['libra_shell = libra.cli.libra_shell:main']
    },
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
