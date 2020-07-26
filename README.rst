============
buildaspider
============


A simple, configurable web crawler written in Python.


Designed to be a jumping off point for:

+ undesrstanding and implementing a crawler
+ parsing markup with `bs4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/BeautifulSoup>`_
+ working with `requests <https://requests.readthedocs.io/en/master/>`_


While its aims are more educational than industrial, it may still be suitable for crawling sites of moderate size (<1000 unique pages). 


Written such that it can either be used as-is for small sites, or extended for any number of crawling applications.


=====
Usage
=====


.. code-block:: python

    from buildaspider import Spider

    myspider = Spider('/path/to/cfg.ini')

    myspider.weave()


=========
Resources
=========


**Official Retry Documentation**

https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry


**Advanced usage of Python requests - timeouts, retries, hooks**

https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure


**Python stdlib Logging: basicConfig**

https://docs.python.org/3.8/library/logging.html#logging.basicConfig


**BFS / FIFO Queue**

https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode


**Python: A quick introduction to the concurrent.futures module**

http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html
