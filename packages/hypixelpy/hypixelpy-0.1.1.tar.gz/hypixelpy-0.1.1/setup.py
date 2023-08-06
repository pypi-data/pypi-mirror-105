import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hypixelpy",
    version="0.1.1",
    author="cinget",
    author_email="evertonpassine@gmail.com",
    description="A simple wrapper for Hypixel API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cinget/hypixelpy",
    project_urls={
        "Bug Tracker": "https://github.com/cinget/hypixelpy/issues",
        "Wiki": "https://github.com/cinget/hypixelpy/wiki",
    },
    classifiers=[
        "Programming Language :: Python :: 3 ",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "": ["*.json"],
    },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)