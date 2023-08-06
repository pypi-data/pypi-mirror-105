import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-test-pkg-tnfru",
    version="0.0.6",
    author="Lars Mueller",
    author_email="lars.lmueller@gamil.com",
    description="Brief test pkg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},

    install_requires=[
        'tensorflow>=2.4.0',
        'ray[tune]'
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

