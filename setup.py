from setuptools import setup, find_packages

setup(
    name="rpi_bootloader_tool",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "rpi-bootloader-tool=rpi_bootloader_tool.main:main"
        ]
    },
    author="Dein Name",
    description="A tool to download and build Raspberry Pi Bootloader and EEPROM.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
