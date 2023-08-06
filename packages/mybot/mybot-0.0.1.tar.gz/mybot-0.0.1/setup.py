import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mybot",
    version="0.0.1",
    author="Yaser Jaradeh",
    author_email="yaser.jaradeh@gmail.com",
    description="MyBot package for creating custom bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YaserJaradeh/mybot",
    project_urls={
        "Bug Tracker": "https://github.com/YaserJaradeh/mybot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)