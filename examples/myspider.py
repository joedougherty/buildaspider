from buildaspider import Spider, append_line_to_log


broken_links_logpath = 'broken_links.log'


class MySpider(Spider):
    # Override this method to login if required!
    def login(self):
        pass

    # Override this method to extend logging!
    def log_broken_link(self, link):
        append_line_to_log(
            broken_links_logpath, 
            f'{link} :: {link.http_code}'
        )


myspider = MySpider('cfg.ini')

myspider.weave()  
