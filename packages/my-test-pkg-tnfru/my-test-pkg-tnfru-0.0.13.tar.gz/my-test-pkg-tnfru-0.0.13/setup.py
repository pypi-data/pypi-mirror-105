import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my-test-pkg-tnfru",
    version="0.0.13",
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
        'numpy~=1.19.2',
        'tensorflow>=2.4.0',
        'ray[tune]',
        'matplotlib',
        'wandb',
        'focal_loss',
        'pillow'
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6.5",
)

