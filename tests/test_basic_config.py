from buildaspider import SpiderConfig


BASIC_CONFIG = 'test_config/basic.ini' 

myconfig = SpiderConfig(BASIC_CONFIG)


def test_log_dir_is_set():
    assert myconfig.log_dir == '/home/joe/buildaspider/tests/test_logs'

