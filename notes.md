Features of Note
================

* pip installable
* short, clean, configurable code
* multi-threading out of the box
* can be used as a library
    * customize by implementing/overriding methods

Theory:

---

* Breadth First Search 


BFS starts at the root node and proceeds by visiting its immediate neighbor nodes.


The first page we visit is the root node.


To discover our nearest neighbors, `gather_links()`:


    def gather_links(self, markup, current_url):
        gathered_links = list()

        for elem in BeautifulSoup(markup, "html.parser").find_all("a"):
            try:
                href = elem["href"]
            except KeyError:
                # Skip any <a> tags missing the "href" attribute.
                continue

            if href != current_url and self.keep_link(href):
                gathered_links.append(
                    Link(current_url, href, elem.text, cfg=self.cfg)
                )

        return gathered_links
    

Also long as the element meets these conditions, it is added to the return list:

* element must have the `href` attribute 
* href must not be the current url
* href must pass `keep_link()` (can't be a broken link, link that threw an exception, or a link that has been visited already):


    def keep_link(self, href):
        if any(
            (
                href in self.broken_urls,
                href in self.exception_urls,
                href in self.visited_urls,
            )
        ):
            return False
        else:
            return True


These are the candidates for the closest neighbors.

If a link is internal (`.worth_visiting == True`) and it hasn't been visited yet, it is a node!

It is added to the visit_queue.



* Inheritance

Python-specific Topics:

---

* concurrent.futures
* configuring requests for retries
* basicConfig
* `__hash__` method


Possible customization Ideas:

---

* Configure/Override default checked/broken link output
* Configure/Override default logging behavior


Resources:

---


Official Retry Documentation:
https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry


Advanced usage of Python requests - timeouts, retries, hooks:
https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure


Logging basicConfig
https://docs.python.org/3.8/library/logging.html#logging.basicConfig


BFS / FIFO Queue
https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
