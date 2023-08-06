import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="zcc-utils",
    version="0.0.1",
    author="zcc",
    author_email="ccz411@outlook.com",
    description="A uitls package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/week233/zcc_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)