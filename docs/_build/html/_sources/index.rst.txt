.. buildaspider documentation master file, created by
   sphinx-quickstart on Sun Sep  6 16:37:04 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to buildaspider's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   src/singlepage.rst


.. toctree::
   :maxdepth: 2
   :caption: A Theoretical Aside:
   
   src/BFS.rst

============
Introduction
============


A simple, configurable web crawler written in Python.


Designed to be a jumping off point for:

+ understanding and implementing your own crawler
+ parsing markup with `bs4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/BeautifulSoup>`_
+ working with `requests <https://requests.readthedocs.io/en/master/>`_


While its aims are more educational than industrial, it may still be suitable for crawling sites of moderate size (<1000 unique pages). 


Written such that it can either be used as-is for small sites, or extended for any number of crawling applications.


**buildaspider** is intended as a platform to learn to build tools for your own quality assurance purposes.

