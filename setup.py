try:
    from setuptools import setup
except ImportError:
    from distuils.core import setup

setup(
    name="buildaspider",
    version='0.6',
    description="Build yourself a small site crawler.",
    author="Joe Dougherty",
    author_email="joseph.dougherty@gmail.com",
    packages=['buildaspider'],
    install_requires=['requests', 'bs4', 'pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
    ],
)
