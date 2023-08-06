from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="as_shinchan",
    version="1.0.0",
    description="A Python package to draw shinchan using turtle",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shivasai-391/as_shinchan",
    author="Alle Shiva Sai",
    author_email="lovelynikki391@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["as_shinchan"],
    include_package_data=True,
)