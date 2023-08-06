from setuptools import setup, find_packages

setup(

    name="rofify",
    version="0.0.1",
    description="Rofi menu script that controls spotify playback.",
    url="https://github.com/dbkosky/rofify.git",
    author="Daniel Kosky",
    author_email="dbkosky@gmail.com",

    py_modules=["rofify"],
    packages=find_packages(),

    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],

    install_requires=["spotipy==2.17.1", "rofi_menu==0.5.1",]

)
