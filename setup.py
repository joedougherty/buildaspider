try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

setup(
    name="buildaspider",
    version='0.1',
    description="Build yourself a small site crawler.",
    author="Joe Dougherty",
    author_email="joseph.dougherty@gmail.com",
    packages=['buildaspider'],
    install_requires=['requests', 'bs4'],
)

