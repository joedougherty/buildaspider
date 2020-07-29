from buildaspider import Spider


BASIC_CONFIG = 'test_config/basic.ini' 


def test_find_broken_links():
    myspider = Spider(BASIC_CONFIG)

    myspider.weave()
