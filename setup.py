from setuptools import find_packages, setup


# Function to parse requirements from a file
def parse_requirements(filename):
    with open(filename, "r") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


setup(
    name="comfy-tweaker",
    version="0.1.0",
    description="A ComfyUI companion app for generating massive amounts of images with precise, user-defined tweaks.",
    author="Nathan Halko",
    author_email="nathan.halko@gmail.com",
    url="https://github.com/halkony/comfy-tweaker",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=parse_requirements("requirements/base.txt"),
    entry_points={
        "console_scripts": [
            "comfy-tweaker=comfy_tweaker.gui:entry",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
