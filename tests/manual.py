from buildaspider import Spider


BASIC_CONFIG = 'test_config/basic.ini' 

myspider = Spider(BASIC_CONFIG)

myspider.weave()
