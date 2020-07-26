====================================================================
A Theoretical Aside: A Practical Application of Breadth-first Search
====================================================================


# The Motivating Question #


*How can we visit all the interconnected pages on a given site?*


One way to model this problem is to consider a website as a kind of graph. 



[Wikipedia]

"It starts at the tree root ... and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level."


BFS:


A. starts at the root node
B. discovers neighboring nodes 
C. proceeds by visiting them and continuing this process until there are no new nodes left to discover and visit


(Wikipedia Pseudocode)[https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode]:


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



It is important to note that we are not searching for a specific node. As such, we do not specify a stop condition (as in lines 7-8 above).


Given that there's no stop condition, we'll explore the graph until the visit queue is empty. We will try to visit every node.


Let's look at how the BFS algorithm is implemented in our `Spider` object.


**A**: We enqueue the seed_urls specified in the config file. This occurs in the `.weave()` method.


The first seed_url is the root of the graph. Let's visit https://joedougherty.github.io.


# TODO -- ROOT IMAGE


    def weave(self):
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


The use of `concurrent.futures.ThreadPoolExecutor` here lets us spawn up to `self.max_workers` to check multiple links at the same time.


The `._update()` method keeps track of checked links, broken links, and links that threw exceptions.


**NOTE**: the iterator returned by `exe.map` retains the original order of the iterable. If I understand this correctly, the calls to `check_link` happen concurrently, but the calls to `._update()` happen one-by-one after the threads have returned. Since the calls to `._update()` are sequential, there is no need to obtain / release locks on the data structures that maintain which links have been visited, are broken, threw exceptions, etc. 


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
* href must not be the current url (prevent infinite `.visit()` loops)
* href must pass `keep_link()` (link can't be: broken link, a link that threw an exception, or a link that has been visited already):

As long as a link is internal (`checked_link.worth_visiting == True`) it is appended to visit_queue.

**C**: The process continues until the visit_queue is empty. 


    while self.visit_queue:
        self.visit(self.visit_queue.pop())


Though our implementation is distributed across a few methods, we can see that all the parts are here and working together.
