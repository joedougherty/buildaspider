import pytest


from buildaspider import SpiderConfig


BASIC_CONFIG = 'test_config/basic.ini' 

myconfig = SpiderConfig(BASIC_CONFIG)


def test_log_dir_is_set():
    assert myconfig.log_dir == '/home/joe/buildaspider/tests/test_logs'


def test_seed_url_is_set():
    assert myconfig.seed_urls == ['http://crawler-test.com/links/broken_links_internal']


def test_include_patterns_set():
    assert myconfig.include_patterns == ['http://crawler-test.com/links/broken_links_internal']


def test_exclude_patterns_set():
    assert myconfig.exclude_patterns == ['^#$', '^javascript']


def test_max_num_retries_is_set():
    assert myconfig.max_num_retries == 5


def test_non_existent_log_dir_throws_exception():
    with pytest.raises(FileNotFoundError):
        myconfig = SpiderConfig('test_config/nonexistentlogdirectory.ini')


def test_missing_login_field():
    assert myconfig.login is None


def test_missing_username_field():
    assert myconfig.username is None


def test_missing_password_field():
    assert myconfig.password is None


def test_missing_login_url_field():
    assert myconfig.login_url is None


def test_config_missing_log_dir():
     with pytest.raises(ValueError):
         myconfig = SpiderConfig('test_config/basic-no-log_dir.ini')


