import setuptools

from metronotation import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metro-notation",
    version=VERSION,
    description="Rubik's cube algorithm visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kitao/metro-notation",
    author="Takashi Kitao",
    author_email="takashi.kitao@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Graphics",
    ],
    packages=[
        "metronotation",
    ],
    install_requires=[
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "metro-notation=metronotation:run",
        ]
    },
)
