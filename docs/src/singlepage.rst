============
Installation
============


.. NOTE::
    It is recommended that you create a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ to facilitate easy management. 


.. TIP:: **Virtual Environment Example**

    First, create the virtual environment.

    
    .. code-block:: python

        python3 -m venv bas_env

    Second, active the virtual environment.

    .. code-block:: python

        source bas_env/bin/activate


**Option 1:**


.. code-block:: text

    pip install buildaspider


**Option 2:**


.. code-block:: text

    git clone git@github.com:joedougherty/buildaspider.git
    cd buildaspider/
    python3 setup.py install



===============
Getting Started
===============

-------------------------------
Step 1: Set Up the Config File
-------------------------------


A config file is **required**. You can copy and paste the example below to get started.


.. code-block:: text

    [buildaspider]

    ; +++ REQUIRED ATTRIBUTES +++ ;

    ; log_dir
    ; seed_urls
    ; include_patterns
    ; exclude_patterns
    ; max_num_retries

    ; Absolute path to directory containing per-run logs
    log_dir = /path/to/logs

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

    ; +++ OPTIONAL ATTRIBUTES +++ ;

    ; login = true 
    ; In order to programatically login, uncomment the line above and ensure login = true
    ;
    ; You will also need to ensure that:
    ;   + the username line is uncommented and set correctly
    ;   + the password line is uncommented and set correctly
    ;   + the login_url line is uncommented and set correctly

    ; username = <USERNAME>
    ; password = <PASSWORD>
    ; login_url = http://example.com/login



Note down the full, absolute path to the config file. This will be the first, required argument to the ``Spider`` instance. See the code sample in the :ref:`basic-usage` section for an example.


-----------------------------------------------
Step 2: Understand What to Expect from Logging 
-----------------------------------------------

.. ATTENTION::

    Ensure that the **log_dir** line is uncommented and that the specified path exists on the file system. 



Each run generates four distinct logs:


+---------------------+---------------------------------+-------------------------------+
| Log                 | Information Provided            | Default Log name pattern      |
+=====================+=================================+===============================+
| Status log          | Status messages                 | ``spider_{now}.log``          |
+---------------------+---------------------------------+-------------------------------+
| Broken links log    | Broken links, HTTP Codes        | ``broken_links_{now}.log``    |
+---------------------+---------------------------------+-------------------------------+
| Checked links log   | All checked links               | ``checked_links_{now}.log``   |  
+---------------------+---------------------------------+-------------------------------+
| Exception links log | Broken links, Exception details | ``exception_links_{now}.log`` |  
+---------------------+---------------------------------+-------------------------------+



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Step 2A: Investigate the ``.setup_logging()`` method [Optional]
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


The log locations are defined in the ``.setup_logging()`` method of the ``Spider`` base class.


.. code-block:: python


    def setup_logging(self):
        now = datetime.now().strftime(self.time_format)

        logging.basicConfig(
            filename=os.path.join(self.log_dir, f"spider_{now}.log"),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.status_logger = logging.getLogger(__name__)

        self.broken_links_logpath = os.path.join(
            self.log_dir, f"broken_links_{now}.log"
        )
        self.checked_links_logpath = os.path.join(
            self.log_dir, f"checked_links_{now}.log"
        )
        self.exception_links_logpath = os.path.join(
            self.log_dir, f"exception_links_{now}.log"
        )


---------------------
Step 3: Verify Setup 
---------------------

The ``Spider`` object provides a ``.verify()`` method that you can use to confirm details.


.. code-block:: python
    
    from buildaspider import Spider


    myspider = Spider('/path/to/config.ini')


    myspider.verify()


This will produce console output similar to the following:


.. code-block:: text 
    

    +-----------------------+-------------------------+
    | ATTRIBUTE             | VALUE                   |
    +-----------------------+-------------------------+
    | Config File           | /home/joe/demo/conf.ini |
    | Log Directory         | /home/joe/demo/logs     |
    | Seed URL              | http://httpbin.org/     |
    | Include Patterns      | ['httpbin.org']         |
    | Exclude Patterns      | ['^#$', '^javascript']  |
    | Max Number of Retries | 5                       |
    | Login                 | False                   |
    | Max Workers           | 8                       |
    | Time Format           | %Y-%m-%d_%H:%M          |
    +-----------------------+-------------------------+


.. NOTE::
    Only the *first* of the Seed URLs will be listed in the console output.


Now that you have confirmed these values make sense, you are ready to kick off the crawling process!



.. _basic-usage:

===========
Basic Usage
===========


Now that the config file is set up and its settings have been confirmed, it is time to call ``.weave()``.


.. code-block:: python

    from buildaspider import Spider


    myspider = Spider(
        '/path/to/cfg.ini', # Full, absolute path to config file
    )

    myspider.weave()


This will start the web crawling process, beginning with the URLs specified in ``seed_urls`` in the config file.


==================
Beyond Basic Usage
==================

---------------------------
Adding the Ability to Login
---------------------------

You can extend the functionality of **buildaspider** by inheriting from the ``Spider`` class and overriding methods. 


This is how you implement the ability for your spider to programmatically login.


Here's the documentation from the base ``Spider`` class:


.. code-block:: python

    
    def login(self):
        # If your session doesn't require logging in, you can leave this method unimplemented.
        #
        # Otherwise, this method needs to return an instance of `requests.Session`.
        #
        # A new session can be obtained by calling `mint_new_session()`.
        #
        raise NotImplementedError("You'll need to implement the login method.")


Here's an example of a fleshed-out login method to ``POST`` credentials (as obtained from the config file) to the ``login_url``. 


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



.. NOTE::

    For more details on logging in with **requests** see: `<https://pybit.es/requests-session.html>`_.


----------------------------------------------------------
Providing Custom Functionality by Attaching to Event Hooks
----------------------------------------------------------

There are a few events that occur during the crawling process that you may want to attach some additional functionality to.

There are pre-visit and post-visit methods you can override/extend.


+---------------------------------------------------+---------------------------+
| Event                                             | Method                    |
+===================================================+===========================+
| link visit is about to begin                      | ``.pre_visit_hook()``     |
+---------------------------------------------------+---------------------------+
| link visit is about to end                        | ``.post_visit_hook()``    | 
+---------------------------------------------------+---------------------------+
| a link has been marked as checked                 | ``.log_checked_link()``   | 
+---------------------------------------------------+---------------------------+
| a link has been marked as broken                  | ``.log_broken_link()``    | 
+---------------------------------------------------+---------------------------+
| a link has been marked as causing an exception    | ``.log_exception_link()`` | 
+---------------------------------------------------+---------------------------+
| crawling is complete                              | ``.cleanup()``            | 
+---------------------------------------------------+---------------------------+



``.pre_visit_hook()`` provides the ability to run custom code when ``.visit()`` is called. 

Code specified in ``.pre_visit_hook()`` will execute prior to library-provided functionality in ``.visit()``. 

``.post_visit_hook()`` provides the ability to run code right before ``.visit()`` returns.


The overridden methods ``.pre_visit_hook()`` and ``.post_visit_hook()`` ought to pass in ``link`` in order to keep the current link in scope and available as a variable with that name. 


------------------


Here is an example that demonstrates storing visited links in a custom container:


.. code-block:: python


    custom_visited_links = list()
    
    def pre_visit_hook(self, link):
        # The `link` being referenced here
        # is the link about to be visited
        custom_visited_links.append(link)



.. Warning::

    This provides direct access to the current ``link`` object in scope. 


If you intend to mutate the ``link`` in scope, a safer strategy is to make a copy ``deepcopy``. This will help prevent you from inadvertently mutating the original ``link`` object.


.. code-block:: python



    from copy import deepcopy
    

    custom_visited_links = list()


    def pre_visit_hook(self, link):
        current_link_copy = deepcopy(link) 
        custom_visited_links.append(current_link_copy)



---------------------------------------
Extending/Overriding Pre-Defined Events 
---------------------------------------


By default, broken links are logged to the location specified by ``.broken_links_logpath``.

We can see this in the ``Spider`` class:


.. code-block:: python

    def log_broken_link(self, link):
        append_line_to_log(self.broken_links_logpath, f'{link} :: {link.http_code}')



What if you want to *extend* (not merely override) the functionality of ``.log_broken_link()``?



.. code-block:: python

    def log_broken_link(self, link):
        super().log_broken_link(link)  
        # You've now retained the original functionality 
        # by running the method as defined on the parent instance

        # Perhaps now you want to: 
        #   + cache this value?
        #   + run some action(s) as a result of this event firing?
        #   + ???



======================
Running the Test Suite
======================

.. NOTE::
    You will need to ensure that the ``log_dir`` config file field is set correctly before you run the test suite. 


.. code-block:: text


    cd tests/
    pytest


====================
Additional Resources
====================

`Official Retry Documentation <https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry>`_

`Advanced usage of Python requests - timeouts, retries, hooks <https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure>`_

`Python stdlib Logging: basicConfig <https://docs.python.org/3.8/library/logging.html#logging.basicConfig>`_

`BFS / FIFO Queue Pseudocode <https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode>`_

`Python: A quick introduction to the concurrent.futures module <http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html>`_

`Using Python Requests on a Page Behind a Login <https://pybit.es/requests-session.html>`_

`The Official collections.deque Documentation <https://docs.python.org/3.8/library/collections.html#collections.deque>`_
