import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FuncToWav", # Replace with your own username
    version="1.0.2",
    author="YeounJun Park",
    author_email="pyj4104@hotmail.com",
    description="Given function, outputs wav file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyj4104/FuncToWav",
    project_urls={
        "Bug Tracker": "https://github.com/pyj4104/FuncToWav/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=[
        "FuncToWav",
    ],
    python_requires=">=3.8",
)
