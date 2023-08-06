import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cycle_analysis", # Replace with your own username
    version="0.0.1",
    author="felixk1990",
    author_email="felixuwekramer@protonmail.com",
    description="cycle_analysis module, performing minimal cycle basis calculation and cycle coalescecne.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felixk1990/cycle-coalescence-algorithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
