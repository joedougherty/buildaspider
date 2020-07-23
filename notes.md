Features of Note
================

* pip installable
* short, clean, configurable code
* can be used as a library
    * customize by implementing/overriding methods
* multi-threading out of the box

Theory:

---

* Breadth-first Search 


BFS:

A. starts at the root node
B. discovers neighboring nodes 
C. proceeds by visiting them and continuing this process until there are no new nodes left to visit/discover


Wikipedia Pseudocode:


	1  procedure BFS(G, root) is
	2      let Q be a queue
	3      label root as discovered	
	4      Q.enqueue(root)			
	5      while Q is not empty do
	6          v := Q.dequeue()
	7          if v is the goal then
	8              return v
	9          for all edges from v to w in G.adjacentEdges(v) do
	10             if w is not labeled as discovered then
	11                 label w as discovered
	12                 w.parent := v
	13                 Q.enqueue(w)



**A**: We enqueue the seed_urls specified in the config file. This occurs in the `.run()` method.


    def run(self):
        for seed_url in self.cfg.seed_urls:
            self.visit_queue.add(Link(None, seed_url, None, cfg=self.cfg))

        try:
            while self.visit_queue:
                self.visit(self.visit_queue.pop())
        finally:
            self.session.close()

            self.status_logger.info("Crawling complete.")


Here's what it looks like when we `.visit()` a link:


    def visit(self, link):
        resp = self.session.get(link.href)

        self.visited_urls.add(link.href)

        gathered_links = self.gather_links(resp.content, link.href)

        packaged_links = [(self.session, link) for link in gathered_links]

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            for result in exe.map(check_link, packaged_links):
                self._update(result)


**B**: Discovering the nearest neighbors is achieved with `gather_links()`:


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
    

If an element meets these conditions, it is added to the list:

* element must have the `href` attribute 
* href must not be the current url
* href must pass `keep_link()` (can't be a broken link, a link that threw an exception, or a link that has been visited already):

As long as a link is internal (`checked_link.worth_visiting == True`) it is appended to visit_queue.

**C**: The process continues until the visit_queue is empty. 


    while self.visit_queue:
        self.visit(self.visit_queue.pop())


Though our implementation of the algorithm is spread across a few methods, we can see that all the parts are here and working together.



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
