from buildaspider import Spider


BASIC_CONFIG = 'test_config/basic.ini' 

myspider = Spider(BASIC_CONFIG)

myspider.weave()

#
# In this example, we are restricting the spider to this one URL
#
def test_single_url_crawl_stopped_did_not_wander_off():
    assert(
        myspider.visited_urls == {'http://crawler-test.com/links/broken_links_internal'}
    )


def test_single_url_found_all_broken_links():
    # http://crawler-test.com/links/broken_links_internal
    assert(
        myspider.broken_links == {
            'http://crawler-test.com/links/not_found/foo4', 
            'http://crawler-test.com/links/not_found/foo1', 
            'http://crawler-test.com/links/not_found/foo2', 
            'http://crawler-test.com/links/not_found/foo3', 
            'http://crawler-test.com/links/not_found/foo5'
        }
    )
