from setuptools import setup, find_packages

setup(
    name="vector-swizzling",
    version="0.1.2",
    packages=find_packages(where="src"),  # Discover packages under 'src'
    package_dir={"": "src"},  # Root directory is 'src'
    install_requires=[],
    description="A versatile vector operations module with swizzling capabilities for 2D, 3D, and 4D vectors.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Isaac Arcia",
    author_email="i.arcia135@gmail.com",
    url="https://github.com/ikz87/python-vector-swizzling",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
