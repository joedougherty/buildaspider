============
buildaspider
============


A simple, configurable web crawler written in Python.


Designed to be a jumping off point for:

+ understanding and implementing a crawler
+ parsing markup with `bs4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/BeautifulSoup>`_
+ working with `requests <https://requests.readthedocs.io/en/master/>`_


While its aims are more educational than industrial, it may still be suitable for crawling sites of moderate size (<1000 unique pages). 


Written such that it can either be used as-is for small sites, or extended for any number of crawling applications.


**buildaspider** is intended as a platform to learn to build tools for your own quality assurance purposes.


===================
Example Config File
===================


A config file is **required**. In addition to the sample given below, you can find an example file in `examples/cgf.ini`.


.. code-block::

    [buildaspider]

    ; login = true 
    ; In order to programatically login, uncomment the line above and ensure login = True
    ;
    ; You will also need to ensure that:
    ;   + the username line is uncommented and set correctly
    ;   + the password line is uncommented and set correctly
    ;   + the login_url line is uncommented and set correctly

    ; username = <USERNAME>
    ; password = <PASSWORD>
    ; login_url = http://example.com/login

    ; Absolute path to directory containing per-run logs
    ; log_dir = /path/to/logs

    ; Literal URLs to visit -- there must be at least one!
    seed_urls = 
        http://httpbin.org/

    ; List of regex patterns to include
    include_patterns =	
        httpbin.org

    ; List of regex patterns to exclude
    exclude_patterns =
        ^#$
        ^javascript

    max_num_retries = 5



===========
Basic Usage
===========


Once the config file is created and ready to go, it is time to create a **Spider** instance.


.. code-block:: python

    from buildaspider import Spider


    myspider = Spider(
        '/path/to/cfg.ini',
        # These are the default settings
        max_workers=8,
        time_format="%Y-%m-%d_%H:%M",
    )

    myspider.weave()


This will start the web crawling process, beginning with the URLs specified in **seed_urls** in the config file.


=======
Logging
=======


By default, each run generates four logs:


+ status log
+ broken links log
+ checked links log
+ exception links log 


The implementation lives in the  **setup_logging** method of the **Spider** base class:


.. code-block:: python


    def setup_logging(self):
        now = datetime.now().strftime(self.time_format)

        logging.basicConfig(
            filename=os.path.join(
                self.cfg.log_dir, 
                "spider_{}.log".format(now)
            ),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.status_logger = logging.getLogger(__name__)

        self.broken_links_logpath = os.path.join(
            self.cfg.log_dir, "broken_links_{}.log".format(now)
        )
        self.checked_links_logpath = os.path.join(
            self.cfg.log_dir, "checked_links_{}.log".format(now)
        )
        self.exception_links_logpath = os.path.join(
            self.cfg.log_dir, "exception_links_{}.log".format(now)
        )



There are three rudimentary methods provided that write to each of the above logs:


+ **log_checked_link**
+ **log_broken_link**
+ **log_exception_link**


For example:


.. code-block:: python

    def log_checked_link(self, link):
        append_line_to_log(self.checked_links_logpath, f'{link}')


This can be overridden to extend logging capabilities. 


These methods can also can be overriden to trigger custom behavior when:

+ a link is checked
+ a broken link is found
+ a link that threw an exception is found


==================
Beyond Basic Usage
==================


You can extend the functionality of **buildaspider** by inheriting from the **Spider** class and overriding methods. 


This is how you implement the ability for your spider to programmatically login.


Here's the documentation from the base **Spider** class:


.. code-block:: python

    
    def login(self):
        #
        # This method needs to return an instance of `requests.Session`.
        #
        # A new session can be obtained by calling `mint_new_session()`.
        #
        raise NotImplementedError("You'll need to implement the login method.")



Here's an example of a fleshed-out login method to **POST** credentials (as obtained from the config file) to the login_url. (For more details on logging in with **requests** see: `<https://pybit.es/requests-session.html>`_.)



.. code-block:: python

    from buildaspider import Spider, mint_new_session, FailedLoginError


    class MySpider(Spider):
        def login(self):
            new_session = mint_new_session()

            login_payload = {
                'username': self.cfg.username,
                'password': self.cfg.password,
            }

            response = new_session.post(self.cfg.login_url, data=login_payload)
            
            if response.status_code != 200:
                raise FailedLoginError("Login Failed :(")

            return response
        


    myspider = MySpider('/path/to/cfg.ini')

    myspider.weave()


====================
Additional Resources
====================


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


**Using Python Requests on a Page Behind a Login**

https://pybit.es/requests-session.html
