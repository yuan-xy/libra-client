import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libra-client",
    version="0.0.1",
    author="yuan xinyu",
    author_email="yuanxinyu.hangzhou@gmail.com",
    description="A python client for Libra network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuan-xy/libra-client.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'canoser==0.1.1'
        'grpcio'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)