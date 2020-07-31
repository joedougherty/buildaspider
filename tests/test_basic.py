from buildaspider import Spider


basic_spider = Spider('test_config/basic.ini')

basic_spider.weave()

#
# In this example, we are restricting the spider to this one URL
#
def test_single_url_crawl_stopped_did_not_wander_off():
    assert(
        basic_spider.visited_urls == {'http://crawler-test.com/links/broken_links_internal'}
    )


def test_single_url_found_all_broken_links():
    # http://crawler-test.com/links/broken_links_internal
    assert(
        basic_spider.broken_urls == {
            'http://crawler-test.com/links/not_found/foo4', 
            'http://crawler-test.com/links/not_found/foo1', 
            'http://crawler-test.com/links/not_found/foo2', 
            'http://crawler-test.com/links/not_found/foo3', 
            'http://crawler-test.com/links/not_found/foo5',
        }
    )


basic_spider_external_links = Spider('test_config/basic2.ini')

basic_spider_external_links.weave()


def test_single_url_crawl_stopped_did_not_wander_off_external_links():
    assert(
        basic_spider_external_links.visited_urls == {'http://crawler-test.com/links/page_with_external_links'}
    )
