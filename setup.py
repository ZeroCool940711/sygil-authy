import os

from setuptools import find_packages, setup

# read the program version from version.py (without loading the module)
# __version__ = run_path('src/sygil_authy/version.py')['__version__']
from src.sygil_authy import __version__


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sygil-authy",
    version=__version__,
    author="Alejandro Gil",
    author_email="alejandrogilelias940711@gmail.com",
    description="Elevate your online security with Sygil Authy, a robust and user-friendly 2FA application.",
    license="proprietary",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"sygil_authy": ["res/*"]},
    long_description=read("README.md"),
    install_requires=["pyotp", "qrcode", "Pillow"],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pre-commit",
    ],
    platforms="any",
    python_requires=">=3.8",
)
