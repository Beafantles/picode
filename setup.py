import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig
from setuptools import setup

current_dir = os.path.dirname(__file__)


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


with open(os.path.join(current_dir, "README.md"), "r", encoding="utf8") as file:
    long_description = file.read()

setup(
    name="picode",
    version="1.1.1",
    description="A module for creating nice pictures of code",
    long_description=long_description,
    url="https://github.com/Beafantles/picode",
    author="Beafantles",
    author_email="beafantles@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows", "Operating System :: POSIX",
        "Programming Language :: Python"
    ],
    keywords="picture image code converter conversion",
    project_urls={
        "Documentation": "https://github.com/Beafantles/picode/wiki",
        "Source": "https://github.com/Beafantles/picode",
        "Bug Reports": "https://github.com/Beafantles/picode/issues"
    },
    install_requires=["pillow", "pygments"],
    python_requires=">=3",
    packages=["picode"],
    # So the file .pypirc can be located in the current directory
    cmdclass={
        "register": register,
        "upload": upload,
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['picode = picode:run_main'],
    })
