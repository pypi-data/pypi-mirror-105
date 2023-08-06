import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="checksum-Pmk456", # Replace with your own username
    version="2.1",
    author="Patan Musthakheem",
    author_email="patanmusthakheem786@gmail.com",
    description="Checksum Is Used For checking File Integrity And Matching With Given Hashes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmk456/checksum",
    project_urls={
        "Bug Tracker": "https://github.com/pmk456/checksumissues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
