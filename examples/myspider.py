from buildaspider import Spider


broken_links_logpath = 'broken_links.log'


class MySpider(Spider):
    def login(self):
        pass

    # Override!
    def log_broken_link(self, link):
        with open(broken_links_logpath, "a") as f:
            f.write("{} :: {}\n\n".format(link.http_code, link))


myspider = MySpider('cfg.ini')

myspider.weave()  
